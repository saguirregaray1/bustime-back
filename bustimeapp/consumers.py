import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import requests



class LiveBustopConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_data(self):
        while True:
            # Replace 'your_api_endpoint' with your actual API endpoint
            response = requests.get('https://catfact.ninja/fact') # TEST endpoint
            
            data = response.json()  # Assuming the response is JSON
            await self.send(text_data=json.dumps(data))
            await asyncio.sleep(30)  # Pause for 30 seconds

    async def receive(self, text_data):
        await self.send_data()
