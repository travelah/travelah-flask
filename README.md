```chatType``` is to define what type of chat should be displayed

```
`0` -> text chat
`1` -> text chat + button
`2` -> text chat + maps
`3` -> text chat (follow up recommender)
```
```altIntent``` is to define what option (fallback/recommended question) should be displayed

```places``` is to give information about the recommended place and coordinate

```predictedResponse``` is to display predicted response from the model

# Examples
```
http://127.0.0.1:5000/predict
```

If intent is predicted correctly (```chatType: 0```)
### Input:
```
{
  "userUtterance": "hello"
}
```
### Output:

```
{
    "altIntent1": null,
    "altIntent2": null,
    "chatType": 0,
    "places": [],
    "predictedResponse": "Hey there! Let's embark on an Indonesian journey together! I'm your virtual guide, excited and ready to go!"
}
```
If intent is not predicted correctly (```chatType: 1```)
### Input:
```
{
  "userUtterance": "medicine"
}
```
### Output:

```
{
    "altIntent1": "Recommend me something",
    "altIntent2": "You are good",
    "chatType": 1,
    "places": [],
    "predictedResponse": "Sorry. I don't know what you just said. Do you mean one of these?"
}
```
# Recommender Examples
If all entities are detected (```region```, ```food_preference```, ```hotel_preference```, ```att_preference```) (```chatType: 2```)

### Input:
```
{
  "userUtterance":"i want to go to ubud to see some art performances an enjoying indonesian food. I want to stay at hotel with swimming pool also."
}
```
Output:

```
{
    "altIntent1": null,
    "altIntent2": null,
    "chatType": 2,
    "places": [
        {
            "lat": -8.490487,
            "lng": 115.2535151,
            "place": "Best Tattoo Ubud"
        },
        {
            "lat": -8.513845,
            "lng": 115.2605567,
            "place": "Handep Flagship Store"
        },
        {
            "lat": -8.5099276,
            "lng": 115.2584608,
            "place": "The Sender Pool Suites"
        },
        {
            "lat": -8.508572899999999,
            "lng": 115.2642564,
            "place": "In Da Compound Warung"
        }
    ],
    "predictedResponse": "Great! Here's your itinerary for your trip:\nDay 1-4: Ubud\nWhen you are in Ubud, the Best Place to Stay based on your preference is in the The Sender Pool Suites or any other hotel of your choice. You can enjoy art by exploring the Best Tattoo Ubud and Handep Flagship Store. For food preferences, you can try eating at In Da Compound Warung."
}
```

#### If not all entities are detected, need follow up questions (```chatType: 3```)
Input:
```
{
  "userUtterance":"recommend me something in ubud"
}
```
Output:

```
{
    "altIntent1": null,
    "altIntent2": null,
    "chatType": 3,
    "places": [],
    "predictedResponse": "Can you specify the attractions you are interested in? (examples: beach, art performance, museum, etc.)"
}
```