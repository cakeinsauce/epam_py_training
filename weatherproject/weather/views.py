from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# fmt: off
from .serializers import ForecastSerializer, RegistrationSerializer
from .services import (get_cities_forecasts_for_period, get_city_forecasts,
                       get_from_cache, write_to_csv)
from .utils import period_params_validate, temp_param_validate

# fmt: on

# TODO: Find out what to do with query params validation and exceptions


@api_view(["GET"])
@permission_classes([AllowAny])
def index(request) -> Response:
    """Index page."""
    return Response({"message": "Simple as fukkk API weather service"})


@api_view(["POST"])
@permission_classes([AllowAny])
def registration(request) -> Response:
    """Register new user."""
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data["status"] = "new user has been created"
        data["email"] = account.email
        data["username"] = account.username
        token = Token.objects.get(user=account).key
        data["auth_token"] = token
    else:
        data = serializer.errors
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@cache_page(settings.CACHE_TTL)
def city_weather(request, city: str) -> Response:
    """City forecast"""
    units = temp_param_validate(request.GET.dict())
    city_forecast = get_city_forecasts(city, units)

    try:
        serializer = ForecastSerializer(city_forecast)
        return Response(serializer.data)
    except KeyError:
        return Response(
            {"message": "cant find that city"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@cache_page(settings.CACHE_TTL)
def largest_cities_weather_download(request) -> HttpResponse:
    """Download largest cities forecasts"""
    params = request.GET.dict()
    units = temp_param_validate(params)
    start, finish = period_params_validate(params)

    cities_forecasts_from_cache = get_from_cache("cities_forecasts")

    try:
        cities_forecasts = get_cities_forecasts_for_period(
            cities_forecasts_from_cache, start, finish, units
        )
    except RuntimeError:  # Cities forecasts are not cached. Run celery and celery-beat!
        return HttpResponse(
            {"message": "cities data is not ready, try it later"}, status=404
        )

    return write_to_csv(cities_forecasts)
