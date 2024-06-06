from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from .models import Stop


class StopSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="sid")

    class Meta:
        model = Stop
        fields = ["id", "lat", "lng"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    favourite_stops = StopSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name", "favourite_stops"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def _add_fav_stops(self, favourite_stops, user):
        for stop in favourite_stops:
            try:
                stop_obj = Stop.objects.get(id=stop.id)
                user.favourite_stops.add(stop_obj)
            except:
                raise serializers.ValidationError(
                    f"Stop with id {stop.id} does not exist."
                )

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        favourite_stops = validated_data.pop("favourite_stops", [])
        user = get_user_model().objects.create_user(**validated_data)
        self._add_fav_stops(favourite_stops, user)
        return user

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs
