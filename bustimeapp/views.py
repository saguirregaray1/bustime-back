from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from django.conf import settings
import requests


def get_token():

    headersList = {
    "Accept": "/",
    "User-Agent": "*",
    "Content-Type": "application/x-www-form-urlencoded" 
    }

    payload = f"grant_type=client_credentials&client_id={settings.CLIENT_ID}&client_secret={settings.CLIENT_SECRET}"

    token = None

    try:
        response = requests.request("POST", settings.TOKEN_URL, data=payload,  headers=headersList)
        token = response.json()['access_token']
    except Exception:
        pass

    return token

def get_request(token, api_url, endpoint, params=None):
    req_params = {}
    if params is not None:
        req_params = params

    response = requests.get(api_url + endpoint, headers = {
            'Authorization': f'Bearer {token}',
            "Accept": "/",
            "User-Agent": "*",
            "Content-Type": "application/x-www-form-urlencoded"
        },params=req_params)
    
    return response
class GetBusesView(APIView):
    def get(self, request):
        buses = None
        try:
            token = get_token()
            response = get_request(token, settings.API_URL, settings.BUSES_ENDPOINT)
            if response.status_code < 300:
                buses = response.json()
            
        except Exception:
            pass

        return Response(buses)
    
