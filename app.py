import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import tensorflow_hub as hub
import tensorflow_text as text
from official.nlp import optimization
from flask import Flask, request, jsonify
import os
import shutil
tf.get_logger().setLevel('ERROR')
import json
import os
import h5py

app = Flask(__name__)

with open('./data/intents.json', 'r') as file:
    intents_data = json.load(file)

loss = tf.keras.losses.CategoricalCrossentropy(from_logits=False)
optimizer = tf.keras.optimizers.Adam(1e-5)
model_filename = "model/travelahAlbertCNN.h5"
loaded_model = load_model(model_filename, custom_objects={'KerasLayer': hub.KerasLayer}, compile=False)
loaded_model.compile(optimizer=optimizer, loss=loss)

@app.route('/predict', methods=['POST'])
def predict_response():
    user_utterance = request.json['user_utterance']

    predictions = loaded_model.predict([user_utterance])
    predicted_intent_index = np.argmax(predictions)
    predicted_intent_probability = float(predictions[0][predicted_intent_index])

    for intent in intents_data['intent']:
        if intent['intent_encoding'] == str(predicted_intent_index):
            predicted_intent = intent['intent']
            predicted_responses = intent['responses'][0]
            break
    else:
        predicted_intent = ""
        predicted_responses = ""
    

    if predicted_intent_probability < 0.25:
        sorted_indices = np.argsort(predictions)[0][::-1]
        first_intent_index = sorted_indices[0]
        second_intent_index = sorted_indices[1]
        first_intent = intents_data['intent'][first_intent_index]['alias']
        second_intent = intents_data['intent'][second_intent_index]['alias']
        predicted_intent = None
        predicted_responses = "Sorry. I don't know what you just say. Do you mean one of this?"

    else:
        first_intent = None
        second_intent = None
    
    response = {
            "predicted_intent": predicted_intent,
            "predicted_response": predicted_responses,
            "alt_intent_1": first_intent,
            "alt_intent_2": second_intent,
        }

    return jsonify(response)


@app.route('/flask', methods=['GET'])
def index():
    return "Flask server"


if __name__ == '__main__':
    app.run( debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)) )
