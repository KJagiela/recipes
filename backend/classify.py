import requests

url = "https://api.spoonacular.com/food/products/classifyBatch?apiKey=1cb977057d9f4456ab6f592930290b8e"

querystring = {"locale":"en_us"}

payload = [
  {
    "title": "onion",
    "upc": "",
    "plu_code": ""
  }
]
headers = {
    'content-type': "application/json",
    'x-rapidapi-key': "",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

response = requests.post(url, json=payload, headers=headers)

print(response.json())