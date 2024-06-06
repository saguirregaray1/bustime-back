from rest_framework import status, viewsets, generics, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


import requests

from django.conf import settings
from .models import Stop
from .serializers import StopSerializer, UserSerializer, AuthTokenSerializer
from drf_spectacular.utils import extend_schema


def get_token():

    headersList = {
        "Accept": "*/*",
        "User-Agent": "*",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = f"grant_type=client_credentials&client_id={settings.CLIENT_ID}&client_secret={settings.CLIENT_SECRET}"
    token = None

    try:
        response = requests.request(
            "POST", settings.TOKEN_URL, data=payload, headers=headersList
        )
        token = response.json()["access_token"]
    except Exception:
        pass

    return token


def get_request(token, api_url, endpoint, params=None):
    req_params = {}
    if params is not None:
        req_params = params

    response = requests.get(
        api_url + endpoint,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "/",
            "User-Agent": "*",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        params=req_params,
    )

    return response


class GetBusesView(APIView):
    def get(self, request):
        buses = None
        try:
            token = get_token()
            response = get_request(token, settings.API_URL, settings.BUSES_ENDPOINT)
            if response.status_code < 300:
                buses = response.json()

        except Exception as e:
            print(e)
            pass

        return Response(buses)


class GetStopsView(APIView):
    def get(self, request):
        stops = None
        token = get_token()

        print(settings.API_URL, settings.STOPS_ENDPOINT)
        response = get_request(token, settings.API_URL, settings.STOPS_ENDPOINT)

        if response.status_code < 300:
            stops = response.json()

        # try:
        #     response = get_request(token, settings.API_URL, settings.STOPS_ENDPOINT)

        #     if response.status_code < 300:
        #         stops = response.json()
        # except Exception as e:
        #     print(e)
        #     pass

        return Response(stops)


class GetStopInfoView(APIView):
    def get(self, request, *args, **kwargs):
        stop_id = self.kwargs["stop_id"]
        token = get_token()
        stop_info = None

        try:
            response = get_request(
                token, settings.API_URL, f"{settings.STOPS_ENDPOINT}/{stop_id}"
            )

            if response.status_code < 300:
                stop_info = response.json()
        except Exception as e:
            print(e)

        return Response(stop_info)


class StopViewSet(viewsets.ViewSet):

    def get_queryset(self):
        return Stop.objects.all()

    @extend_schema(responses=StopSerializer)
    def list(self, request):
        """
        Endpoint to retrieve all stops
        """
        queryset = self.get_queryset()

        serializer = StopSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=StopSerializer(many=True), responses=StopSerializer(many=True)
    )
    def create(self, request):
        """
        Endpoint to create a new stop
        """
        serializer = StopSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated userr"""
        return self.request.user
