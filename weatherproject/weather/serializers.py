from rest_framework import serializers

from .models import Account, Forecast, Weather


class WeatherSerializer(serializers.ModelSerializer):
    """Weather model serializer"""

    class Meta:
        model = Weather
        fields = [
            "time",
            "status",
            "temperature",
            "pressure",
            "wind_speed",
            "direction",
            "humidity",
            "rain",
            "snow",
        ]


class ForecastSerializer(serializers.ModelSerializer):
    """Forecast model serializer"""

    forecasts = WeatherSerializer(many=True, read_only=True)

    class Meta:
        model = Forecast
        fields = ["reception_time", "location", "unit", "forecasts"]


class RegistrationSerializer(serializers.ModelSerializer):
    """Registration model serializer"""

    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Account
        fields = ["email", "username", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        account = Account(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"status": "passwords must match"})
        account.set_password(password)
        account.save()
        return account
