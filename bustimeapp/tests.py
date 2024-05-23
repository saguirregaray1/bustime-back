from django.test import TestCase
from django.urls import reverse

class YourAppTests(TestCase):
    def test_buses(self):
        # Use reverse to dynamically fetch URL from name given in urls.py
        response = self.client.get(reverse('buses'))
        self.assertEqual(response.status_code, 200)

    def test_stops(self):
        response = self.client.get(reverse('stops'))
        self.assertEqual(response.status_code, 200)

from channels.testing import WebsocketCommunicator
from django.test import ChannelsLiveServerTestCase
from bustimeapp.consumers import LiveBustopConsumer

class MyWebSocketTests(ChannelsLiveServerTestCase):
    async def test_my_consumer(self):
        """
        Tests that the WebSocket connection opens, communicates, and closes as expected.
        """
        # Create a WebSocket communicator connected to the live server
        communicator = WebsocketCommunicator(LiveBustopConsumer.as_asgi(), "/ws/bustop_live/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        
        # Test sending to and receiving from the socket
        await communicator.send_to(text_data="hello")
        response = await communicator.receive_from()
        self.assertIncludes(response, "cat")

        # Close and confirm closure
        await communicator.disconnect()

