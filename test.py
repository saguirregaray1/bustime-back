import requests
import json

url = "http://localhost:8000/bustimeapp/stops"

response = requests.get(url)

response_json = response.json()
data = []
print(len(response_json))
    

