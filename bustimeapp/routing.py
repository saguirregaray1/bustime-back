from django.urls import re_path
from .consumers import LiveBustopConsumer

websocket_urlpatterns = [
    re_path('ws/bustop_live', LiveBustopConsumer.as_asgi()),
]