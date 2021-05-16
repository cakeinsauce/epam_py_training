from rest_framework import serializers

from ..models import Forecast


class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = ["reception_time", "location", "units", "forecasts"]
