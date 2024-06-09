import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import bustimeapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bustime.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(), 
    "websocket": URLRouter(
            bustimeapp.routing.websocket_urlpatterns
        )
})