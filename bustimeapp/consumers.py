import json
from channels.generic.websocket import WebsocketConsumer
import requests


class LiveBustopConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
        self.send(text_data=json.dumps({
            'message': 'Connected'
        }))

    