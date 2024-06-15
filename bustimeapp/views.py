from rest_framework import status, viewsets, generics, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


import requests

from django.conf import settings
from .models import Stop, BusSchedule
from .serializers import StopSerializer, UserSerializer, AuthTokenSerializer, BusScheduleSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter


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
    
    serializer_class = None
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
    serializer_class = None

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
    serializer_class = None
    
    def _get_upcoming_buses(self,token, bus_stop_id, bus_lines):
        upcoming_buses = None
        endpoint = f"{settings.STOPS_ENDPOINT}/{bus_stop_id}/{settings.UPCOMING_BUSES}"
        try:
            response = get_request(token, settings.API_URL, endpoint, params={'lines': ','.join(map(str, bus_lines))})
            if response.status_code < 300:
                upcoming_buses = response.json()
        except Exception:
            pass
        return upcoming_buses
    
    
    def get(self, request, *args, **kwargs):
    
        stop_id = self.kwargs["stop_id"]
        token = get_token()
        stop_info = None

        try:
            url=f"{settings.STOPS_ENDPOINT}/{stop_id}"
            response = get_request(token, settings.API_URL, url)
            
            print(response)

            if response.status_code < 300:
                stop_info = response.json()
                
            bus_lines = stop_info.get("lineas", [])
            upcoming_buses = self._get_upcoming_buses(token, stop_id, bus_lines)
            
            if upcoming_buses is not None:
                stop_info["upcoming_buses"] = upcoming_buses
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
    
class BusScheduleViewSet(viewsets.ViewSet):

    def get_queryset(self):
        return BusSchedule.objects.all()

    @extend_schema(responses=BusScheduleSerializer)
    def list(self, request):
        """
        Endpoint to retrieve all stops
        """
        queryset = self.get_queryset()

        serializer = BusScheduleSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=BusScheduleSerializer(many=True), responses=BusScheduleSerializer(many=True)
    )
    def create(self, request):
        """
        Endpoint to create a new stop
        """
        serializer = BusScheduleSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddFavouriteStopView(APIView):
    """Add a favourite stop to the authenticated user."""

    serializer_class = None
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        operation_id="add_favourite_stop",
        parameters=[
            OpenApiParameter(
                name="stop_id",
                description="ID of the stop to add to favourites",
                required=True,
                type=int,
            ),
        ],
    )
    def post(self, request):
        stop_id = request.query_params.get("stop_id")

        if stop_id is None:
            return Response(
                {"error": "stop_id parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            stop = Stop.objects.get(sid=stop_id)
        except Stop.DoesNotExist:
            return Response(
                {"error": "Stop not found."}, status=status.HTTP_404_NOT_FOUND
            )

        request.user.favourite_stops.add(stop)
        return Response(
            {"message": "Stop added to favourites."}, status=status.HTTP_200_OK
        )


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
