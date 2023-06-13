import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import ast
nltk.download("stopwords")
import re
from nltk.corpus import stopwords as nltk_stopwords

travel_df = pd.read_csv("data/travel_spot_datasets_final_updated_with_region.csv")
hotel_df = pd.read_csv('data/booking_datasets_final_updated_with_region.csv')
food_df = pd.read_csv('data/food_datasets_final_updated_with_region.csv')

clean_spcl = re.compile('[/(){}\[\]\|@,;]')
clean_symbol = re.compile('[^0-9a-z #+_]')
stop_words = set(nltk_stopwords.words('english'))


def clean_df(text):
    if isinstance(text, list):
        text = ' '.join(text)
    text = text.lower()
    text = re.sub("[^a-zA-Z0-9 ]", "", str(text))
    text = clean_spcl.sub(' ', text)
    text = clean_symbol.sub('', text)
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

travel_df = travel_df.drop(["source"],axis=1)
travel_df = travel_df.drop_duplicates(subset='place')
food_df = food_df.drop(["source"],axis=1)
food_df = food_df.drop(["range"],axis=1)
food_df = food_df.drop_duplicates(subset='place_name')
hotel_df = hotel_df.drop(["source_href"],axis=1)
hotel_df = hotel_df.drop_duplicates(subset='name_hotel')

selected_features_travel = ['rating_label', 'review_label','type_category','keywords','formatted_address','region']
selected_features_food = ['rating', 'cuisine','eating_type','price','region','formatted_region','comment','second_comment' ]
selected_features_hotel = ['formatted_region', 'price_label','rating_type','description', 'formatted_address', 'region']

for feature in selected_features_travel:
  travel_df[feature]= travel_df[feature].fillna('')
  travel_df[feature] = travel_df[feature].apply(clean_df)

for feature in selected_features_food:
  food_df[feature]= food_df[feature].fillna('')
  food_df[feature] = food_df[feature].apply(clean_df)

for feature in selected_features_hotel:
  hotel_df[feature]= hotel_df[feature].fillna('')
  hotel_df[feature] = hotel_df[feature].apply(clean_df)

travel_df = travel_df.reset_index(drop=True)
hotel_df = hotel_df.reset_index(drop=True)
food_df = food_df.reset_index(drop=True)

travel_df['combined_text'] = travel_df['place'] + ' ' + travel_df['region'] + ' ' + travel_df['type_category'] + ' ' + travel_df['keywords'] + ' ' + travel_df['formatted_address'] 
food_df['food_clean'] = food_df['formatted_region'] + ' ' + food_df['cuisine'] + ' ' + food_df['rating'] + ' '  + food_df['eating_type'] + ' '+ food_df['price'] + ' '+food_df['region'] + ' '+ food_df['comment'] + ' ' + food_df['second_comment'] 
hotel_df['desc_clean'] = hotel_df['formatted_region'] + ' ' +  hotel_df['price_label'] + ' '+ hotel_df['rating_type'] + ' '  + hotel_df['description'] + ' ' + hotel_df['formatted_address'] + ' '+ hotel_df['region'] 

missing_indices_travel = travel_df['combined_text'].isnull()
if missing_indices_travel.any():
    travel_df.loc[missing_indices_travel, 'combined_text'] = ''

missing_indices_food = food_df['food_clean'].isnull()
if missing_indices_food.any():
    food_df.loc[missing_indices_food, 'food_clean'] = ''

missing_indices_hotel = hotel_df['desc_clean'].isnull()
if missing_indices_hotel.any():
    food_df.loc[missing_indices_hotel, 'food_clean'] = ''

vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), stop_words='english')
tfidf = vectorizer.fit_transform(travel_df['combined_text'])
tfidf_hotel = vectorizer.transform(hotel_df['desc_clean'])
tfidf_food = vectorizer.transform(food_df['food_clean'])

def check_region_travel(region):
    valid_regions = set(travel_df['region'])
    entered_region = clean_df(region.lower())

    for valid_region in valid_regions:
        if entered_region in valid_region:
            return True

    return False

def get_top_recommendations(df, num_recommendations):
    return df.head(num_recommendations)

def generate_itinerary(regions, travel_preferences, hotel_preferences, food_preferences, duration):
    itinerary = "Great! Here's your itinerary for your trip:\n"
    all_recommendations = []
    all_locations = [] 
    num_days_per_region = duration // len(regions)
    remaining_days = duration % len(regions)
    preference_counts = {}

    for preference in travel_preferences:
        category = preference.split(':')[0].strip()
        if category not in preference_counts:
            preference_counts[category] = 0
        preference_counts[category] += 1

    total_recommendations = 0
    num_recommendations_per_category = {}

    for category, count in preference_counts.items():
        num_recommendations_per_category[category] = count
        total_recommendations += count
      
    for i, region in enumerate(regions):
        if i == len(regions) - 1:
            if remaining_days > 0:
                itinerary += f"Day {i*num_days_per_region+1}-{i*num_days_per_region+num_days_per_region+remaining_days}: {region}\n"
                remaining_days -= 1
            else:
                itinerary += f"Day {i*num_days_per_region+1}-{i*num_days_per_region+num_days_per_region}: {region}\n"
        else:
            itinerary += f"Day {i*num_days_per_region+1}-{i*num_days_per_region+num_days_per_region}: {region}\n"

        travel_results = pd.DataFrame()
        for preference, count in num_recommendations_per_category.items():
            travel_results_category = search_travel_spot(region, [preference])
            num_travel_recommendations = min(count, len(travel_results_category))
            num_recommendations = 2 
            top_travel_recommendations = get_top_recommendations(travel_results_category, num_recommendations)
            travel_results = pd.concat([travel_results, top_travel_recommendations], ignore_index=True)

        num_travel_recommendations = min(10, len(travel_results))
        top_travel_recommendations = get_top_recommendations(travel_results, num_travel_recommendations)
        travel_recommendations = top_travel_recommendations.head(6)
        
        if not travel_recommendations.empty:
            itinerary += f"When you are in {region.capitalize()}, the Best Place to Stay based on your preference is in the "
            
            hotel_results = pd.DataFrame()
            hotel_results = search_hotels(region, hotel_preferences)
            num_hotel_recommendations = min(10, len(hotel_results))
            top_hotel_recommendations = get_top_recommendations(hotel_results, num_hotel_recommendations)

            hotel_recommendation = top_hotel_recommendations.head(1)
            
            if not hotel_recommendation.empty:
                hotel_location = hotel_recommendation['location'].iloc[0]
                location = ast.literal_eval(hotel_location)
                all_locations.append({"place": hotel_recommendation['name_hotel'].iloc[0], "lat": location['lat'], "lng": location['lng']})  

                itinerary += f"{hotel_recommendation['name_hotel'].iloc[0]} or any other hotel of your choice. "

                if not travel_recommendations.empty:
                    itinerary += f"You can enjoy {'and '.join(travel_preferences)} by exploring the "
                    for _, spot in travel_recommendations.iterrows():
                        itinerary += spot['place'] + " and "
                        location = ast.literal_eval(spot['location'])
                        all_locations.append({"place": spot['place'], "lat": location['lat'], "lng": location['lng']})  
                    itinerary = itinerary[:-5] + ". "
                else:
                    itinerary += "\n"

                food_recommendations = []
                for food_preference in food_preferences:
                    food_results_category = search_food(region, [food_preference])
                    num_food_recommendations = min(1, len(food_results_category))
                    top_food_recommendations = get_top_recommendations(food_results_category, num_food_recommendations)
                    food_recommendations.extend(top_food_recommendations['place_name'].tolist())

                if food_recommendations:
                    itinerary += f"For food preferences, you can try eating at "
                    for place_name in food_recommendations:
                        itinerary += place_name + ", "
                        place_location = food_df.loc[food_df['place_name'] == place_name, 'location'].iloc[0]
                        location = ast.literal_eval(place_location)
                        all_locations.append({"place": place_name, "lat": location['lat'], "lng": location['lng']})  
                    itinerary = itinerary[:-2] + "."
                else:
                    itinerary += "No food recommendations found.\n\n"
            else:
                itinerary += "No hotel recommendations found.\n\n"
        else:
            itinerary += "No travel recommendations found.\n\n"

        all_recommendations.extend(travel_recommendations['place'].tolist())
        all_recommendations.extend(hotel_recommendation['name_hotel'].tolist())

    all_recommendations.extend(food_recommendations)
    all_recommendations_with_locations = [{"place": recommendation, "lat": next((location['lat'] for location in all_locations if location['place'] == recommendation), 'Unknown lat'), "lng": next((location['lng'] for location in all_locations if location['place'] == recommendation), 'Unknown lng')} for recommendation in all_recommendations]

    return itinerary, all_recommendations_with_locations

def search_travel_spot(region, query):
    query_string = ' '.join(query)
    parameters = query_string.split(',')

    results = pd.DataFrame()

    for preference in parameters:
        query_string = f"{region} {preference.strip()}"
        query_vector = vectorizer.transform([query_string])
        similarity_scores = cosine_similarity(query_vector, tfidf).flatten()

        region_indices = travel_df['region'].str.contains(region, case=False, regex=False)
        category_indices = travel_df['type_category'].str.contains(preference.strip(), case=False, regex=True)
        keywords_indices = travel_df['keywords'].str.contains(preference.strip(), case=False, regex=True)
        rating_indices = travel_df['rating_label'].str.contains(preference.strip(), case=False, regex=True)
        review_indices = travel_df['review_label'].str.contains(preference.strip(), case=False, regex=True)

        filtered_scores = (similarity_scores * region_indices) + (category_indices +rating_indices+ keywords_indices + review_indices)

        top_indices = filtered_scores.argsort()[::-1]
        preference_results = travel_df.iloc[top_indices]
        
        results = pd.concat([results, preference_results], ignore_index=True)

    return results

def search_hotels(region, query):
    query_string = ' '.join(query)
    parameters = query_string.split(',')

    results = pd.DataFrame()

    for preference in parameters:
      query_string = f"{region} {' '.join(parameters)}"
      query_vector = vectorizer.transform([query_string])
      similarity_scores = cosine_similarity(query_vector, tfidf_hotel).flatten()

  
      region_indices = hotel_df['formatted_region'].str.contains(region, case=False, regex=False)
      description_indices = hotel_df['description'].str.contains(preference.strip(), case=False, regex=True)
      price_indices = hotel_df['price_label'].str.contains(preference.strip(), case=False, regex=True)
      rating_indices = hotel_df['rating_type'].str.contains(preference.strip(), case=False, regex=True)

      filtered_scores = (similarity_scores * region_indices) + (description_indices +price_indices+rating_indices)
      top_indices = filtered_scores.argsort()[::-1]
      preference_results = hotel_df.iloc[top_indices]

      results = pd.concat([results, preference_results], ignore_index=True)
    return results

def search_food(region, query):
    query_string = ' '.join(query)
    parameters = query_string.split(',')

    results = pd.DataFrame()
    for preference in parameters:
        query_string = f"{region} {preference.strip()}"
        query_vector = vectorizer.transform([query_string])
        similarity_scores = cosine_similarity(query_vector, tfidf_food).flatten()

        region_indices = food_df['formatted_region'].str.contains(region, case=False, regex=False)
        cuisine_indices = food_df['cuisine'].str.contains(preference.strip(), case=False, regex=True)
        price_indices = food_df['price'].str.contains(preference.strip(), case=False, regex=True)
        rating_indices = food_df['rating'].astype(str).str.contains(preference.strip(), case=False, regex=True)
        review_indices = food_df['comment'].str.contains(preference.strip(), case=False, regex=True)
        eating_type_indices = food_df['eating_type'].str.contains(preference.strip(), case=False, regex=True)
        filtered_scores = (similarity_scores * region_indices) + (cuisine_indices + price_indices + rating_indices + review_indices + eating_type_indices)

        top_indices = filtered_scores.argsort()[::-1]
        preference_results = food_df.iloc[top_indices]
        
        results = pd.concat([results, preference_results], ignore_index=True)
    return results

def check_region_travel(region):
    valid_regions = set(travel_df['region'])
    entered_region = clean_df(region.lower())
    for valid_region in valid_regions:
        if entered_region in valid_region:
            return True

    return False

def main(region_inp, attraction, hotel, food, duration_input):
    region_input_travel = region_inp
    place_input_travel = attraction
    place_input_hotel = hotel
    food_input = food
    duration_input = duration_input

    regions = [region.strip() for region in region_input_travel.split(',')]
    travel_preferences = [travel.strip() for travel in place_input_travel.split(',')]
    hotel_preferences = [hotel.strip() for hotel in place_input_hotel.split(',')]
    food_preferences = [food.strip() for food in food_input.split(',')]
    duration = duration_input
    if len(regions) > 0 and len(travel_preferences) > 0 and len(hotel_preferences) > 0 and len(food_preferences) > 0 and duration > 0:
        valid_regions = []
        for region in regions:
            if check_region_travel(region):
                valid_regions.append(region.strip())

        if valid_regions:
            itinerary, places_coord = generate_itinerary(valid_regions, travel_preferences, hotel_preferences, food_preferences, int(duration))
            return itinerary, places_coord
        else:
            return "Sorry, the entered regions are not valid."
    else:
        return "Please enter valid regions, location/type of place for travel, description/keywords for hotel, food preferences, and duration of travel (in days)."