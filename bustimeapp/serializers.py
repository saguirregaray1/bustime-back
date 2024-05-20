from rest_framework import serializers

from .models import Stop

class StopSerializer(serializers.ModelSerializer):
    stop_sid = serializers.IntegerField(source="sid")
    stop_lat = serializers.FloatField(source="lat")
    stop_lng = serializers.FloatField(source="lng")

    class Meta:
        model = Stop
        fields = ["stop_sid", "stop_lat", "stop_lng"]