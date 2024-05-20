import requests
import json

url = "http://localhost:8000/bustimeapp/stops"

response = requests.get(url)

response_json = response.json()
data = []
for stop in response_json:
    postUrl = "http://localhost:8000/api/stop/"
    body = {"stop_sid": stop['busstopId'],
    "stop_lat": stop['location']['coordinates'][0],
    "stop_lng": stop['location']['coordinates'][1]}
    headers = {'Content-Type': 'application/json'}
    data.append(body)

    
post_response = requests.post(postUrl, json=data, headers=headers)   

