import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import tensorflow_hub as hub
import tensorflow_text as text
from official.nlp import optimization
from flask import Flask, request, jsonify
tf.get_logger().setLevel('ERROR')
from recommender import recommender
import os, json, random

app = Flask(__name__)

with open('./data/intents.json', 'r') as file:
    intents_data = json.load(file)

loss = tf.keras.losses.CategoricalCrossentropy(from_logits=False)
optimizer = tf.keras.optimizers.Adam(1e-5)

model_filename = "model/travelahAlbertCNNFinal.h5"
loaded_model = tf.keras.models.load_model(model_filename, custom_objects={'KerasLayer': hub.KerasLayer}, compile=False)
loaded_model.compile(optimizer=optimizer, loss=loss)

@app.route('/predict', methods=['POST'])
def predict_response():
    user_utterance = request.json['userUtterance'].lower()
    places = []
    predictions = loaded_model.predict([user_utterance])
    predicted_intent_index = np.argmax(predictions)
    predicted_intent_probability = float(predictions[0][predicted_intent_index])

    for intent in intents_data['intent']:
        if intent['intent_encoding'] == str(predicted_intent_index):
            predicted_intent = intent['intent']
            predicted_responses = intent['responses']
            chat_type = 0

            if predicted_intent == "recommender":
                results = recommender(user_utterance)
                if not isinstance(results, str):
                    places =  results[1]
                    itinerary = results[0]
                    predicted_responses = [itinerary]
                    chat_type = 2
                else:
                    predicted_responses = [results]
                    chat_type = 3
            
            predicted_responses = random.choice(predicted_responses)

    first_intent = None
    second_intent = None

    if predicted_intent_probability < 0.40:
        sorted_indices = np.argsort(predictions)[0][::-1]
        first_intent_index = sorted_indices[0]
        second_intent_index = sorted_indices[1]
        first_intent = intents_data['intent'][first_intent_index]['alias']
        second_intent = intents_data['intent'][second_intent_index]['alias']
        predicted_responses = "Sorry. I don't know what you just said. Do you mean one of these?"
        chat_type = 1

    response = {
        "predictedResponse": predicted_responses,
        "altIntent1": first_intent,
        "altIntent2": second_intent,
        "chatType": chat_type,
        "places": places
    }
    return jsonify(response)

@app.route('/flask', methods=['GET'])
def index():
    return "Flask server"

if __name__ == '__main__':
    app.run( debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 3000)) )
