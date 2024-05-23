from rest_framework import serializers

from .models import Stop

class StopSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="sid")

    class Meta:
        model = Stop
        fields = ["id", "lat", "lng"]