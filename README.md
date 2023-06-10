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
    "predictedResponse": "Hi there! Ready to explore Indonesia together? I'm here and excited to be your virtual tour guide."
}
```
#### **If intent is not predicted correctly**
Input:
```
{
  "userUtterance": "jakarta"
}
```
Output:

```
{
    "altIntent1": "Bye",
    "altIntent2": "Tell me about Bali",
    "chatType": 1,
    "predictedResponse": "Sorry. I don't know what you just say. Do you mean one of this?"
}
```
