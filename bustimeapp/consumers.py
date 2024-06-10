import json
from channels.generic.websocket import AsyncWebsocketConsumer
import requests
from .utils import get_token, get_request, get_upcoming_buses
from django.conf import settings
import asyncio

class LiveBustopConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        await self.send(text_data=json.dumps({
            'message': 'Connected'
        }))
        

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        stop_id = text_data_json['stop_id']
        if stop_id is not None:
            await self.send_updates(stop_id)
        
        
    async def disconnect(self, close_code):
        pass
        
    async def send_updates(self, stop_id):    
        token = await get_token()
        url=f"{settings.STOPS_ENDPOINT}/{stop_id}"
        first = True
        while True:  
            stop_info = None
            try:
                if first:
                    first=False
                else:
                    await asyncio.sleep(8)
                response = await get_request(token, settings.API_URL, url)

                if response.status_code >= 300:
                    error_message = response.text
                    if response.status_code == 429:
                        await asyncio.sleep(20)
                    raise Exception(f"Request failed with status {response.status_code}. Message: {error_message}")

                stop_info = response.json()

                bus_lines = stop_info["lineas"]
                upcoming_buses = await get_upcoming_buses(token, stop_id, bus_lines)
                if upcoming_buses is not None:
                    stop_info["upcoming_buses"] = upcoming_buses
                text_data=json.dumps(stop_info)
                await self.send(text_data=text_data)
            except Exception as e:
                print(e)

            
    