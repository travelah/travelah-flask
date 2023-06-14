import spacy
from recommendation import main
import random

nlpReg = spacy.load("model/spacyTravelah/model-reg")
nlpFood = spacy.load("model/spacyTravelah/model-food")
nlpHotel = spacy.load("model/spacyTravelah/model-hotel")
nlpAtt = spacy.load("model/spacyTravelah/model-att")

def follow_up(empty_lists):
    if "region" in empty_lists:
        return "I can do that. Please provide the desired region for your trip"
    elif "attraction" in empty_lists:
        return "Can you specify the attractions you are interested in?"
    elif "hotel" in empty_lists:
        return "I want to know your hotel preferences. Can you mention it?"
    elif "food" in empty_lists:
        return "Please let us know your food preferences."
    else:
        return None

def predict_entities(text):
    models = [nlpReg, nlpFood, nlpHotel, nlpAtt]

    region = []
    food = []
    hotel = []
    attraction = []
    empty_lists = []

    for model in models:
        doc = model(text)
        for entity in doc.ents:
            if entity.label_ == "REGION":
                region.append(entity.text)
            elif entity.label_ == "FOOD_PREFERENCE":
                food.append(entity.text)
            elif entity.label_ == "HOTEL_PREFERENCES":
                hotel.append(entity.text)
            elif entity.label_ == "ATT_PREFERENCE":
                attraction.append(entity.text)

    if not region:
        empty_lists.append("region")
    if not attraction:
        empty_lists.append("attraction")
    if not hotel:
        empty_lists.append("hotel")
    if not food:
        empty_lists.append("food")

    return region, food, hotel, attraction, empty_lists

def recommender(text):
    region, attraction, hotel, food, empty_lists = predict_entities(text)
    follow_up_message = None
    if empty_lists:
        follow_up_message = follow_up(empty_lists)
        if follow_up_message:
            return follow_up_message
    
    region = ', '.join(region) if region else ''
    food = ', '.join(food) if food else ''
    hotel = ', '.join(hotel) if hotel else ''
    attraction = ', '.join(attraction) if attraction else ''
    days = random.randint(2, 7)


    req, places_coord = main(region, food, hotel, attraction, days)

    return req, places_coord

# text = "i want to go to ubud to see some art performances an enjoying indonesian food. I want to stay at hotel with swimming pool also."
# rec, places_coord = recommender(text)
# print(rec)
# print(places_coord)