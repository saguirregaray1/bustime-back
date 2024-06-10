import requests

from django.conf import settings
import httpx



async def get_upcoming_buses(token, bus_stop_id, bus_lines):
    upcoming_buses = None
    endpoint = f"{settings.STOPS_ENDPOINT}/{bus_stop_id}/{settings.UPCOMING_BUSES}"
    headers = {"Authorization": f"Bearer {token}"}
    params = {'lines': ','.join(map(str, bus_lines))}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.API_URL}{endpoint}", headers=headers, params=params)
            if response.status_code < 300:
                upcoming_buses = response.json()
    except Exception:
        pass

    return upcoming_buses

async def get_token():

    headersList = {
        "Accept": "*/*",
        "User-Agent": "*",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = f"grant_type=client_credentials&client_id={settings.CLIENT_ID}&client_secret={settings.CLIENT_SECRET}"
    token = None

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.TOKEN_URL, data=payload, headers=headersList)
            token = response.json()["access_token"]
    except Exception:
        pass

    return token

async def get_request(token, api_url, endpoint, params=None):
    req_params = {}
    if params is not None:
        req_params = params

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "/",
        "User-Agent": "*",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url + endpoint, headers=headers, params=req_params)

    return response