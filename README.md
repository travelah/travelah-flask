### Examples
```
http://127.0.0.1:5000/predict
```
#### **If intent is predicted correctly**
Input:
```
{
  "userUtterance": "hello"
}
```
Output:

```
{
    "altIntent1": null,
    "altIntent2": null,
    "chatType": 0,
    "places": [],
    "predictedResponse": "Hey there! Ready to dive into Indonesia? I'm your virtual guide, thrilled to show you around!"
}
```
#### **If intent is not predicted correctly**
Input:
```
{
  "userUtterance":"medicine"
}
```
Output:

```
{
    "altIntent1": "Hello",
    "altIntent2": "Recommend me something",
    "chatType": 1,
    "places": [],
    "predictedResponse": "Sorry. I don't know what you just said. Do you mean one of these?"
}
```
### **Recommender Examples**
#### **If all entities are detected (region, food_preference, hotel_preference, attraction_preference)**

Input:
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
        "Best Tattoo Ubud",
        "Handep Flagship Store",
        "The Sender Pool Suites",
        "In Da Compound Warung"
    ],
    "predictedResponse": "Great! Here's your itinerary for your trip:\n\nDay 1-7: ubud\nWhen you are in Ubud, the Best Place to Stay based on your preference is in the The Sender Pool Suites or any other hotel of your choice. You can enjoy art by exploring the Best Tattoo Ubudand Handep Flagship Storean. For food preferences, you can try eating indonesian cuisine at the In Da Compound Warung."
}
```

#### **If not all entities are detected**
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
    "chatType": 2,
    "places": [],
    "predictedResponse": "Can you specify the attractions you are interested in?"
}
```