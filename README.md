### Examples
```
http://127.0.0.1:5000/predict
```
#### **If intent is predicted correctly**
Input:
```
{
  "user_utterance": "who are you"
}
```
Output:

```
{
    "alt_intent_1": null,
    "alt_intent_2": null,
    "predicted_intent": "smalltalk_agent_acquaintance",
    "predicted_response": "Hey buddy! I'm Vela, your virtual tour guide for Bali. Ready to explore the beauty and awesomeness of this place? Ask away! Let's go on an epic adventure together!",
    "probability": 0.9692302942276001
}
```
#### **If intent is not predicted correctly**
Input:
```
{
  "user_utterance": "do you know MUSE band?"
}
```
Output:

```
{
    "alt_intent_1": "smalltalk_agent_age",
    "alt_intent_2": "smalltalk_agent_acquaintance",
    "predicted_intent": null,
    "predicted_response": "Sorry. I don't know what you just say. Do you mean one of this?",
    "probability": 0.23114833235740662
}
```
