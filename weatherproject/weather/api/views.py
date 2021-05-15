from pyowm.commons import exceptions as excOWM
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..services import *
from .serializers import ForecastSerializer


@api_view(
    [
        "GET",
    ]
)
def api_city_weather(request, city: str) -> Response:

    try:
        city_forecaster = get_city_forecaster(city)
        units = request.GET.get("u", "celsius")
        city_forecast = get_city_forecasts_five_days(city_forecaster, units)
    except excOWM.APIRequestError:  # OWM network failure
        return Response(status=status.HTTP_408_REQUEST_TIMEOUT)
    except excOWM.NotFoundError:  # Unable to find the city
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ForecastSerializer(city_forecast)
    return Response(serializer.data)
