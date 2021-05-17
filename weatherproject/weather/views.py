from django.conf import settings
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import ForecastSerializer, RegistrationSerializer
from .services import *


@api_view(["GET"])
@permission_classes([AllowAny])
def index(request) -> Response:
    """Index page API."""
    return Response({"message": "Simple as fukkk API weather service"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def city_weather(request, city: str) -> Response:
    """City forecast"""
    units = request.GET.get("u", "celsius")
    start = request.GET.get("s", "0001-01-01_00-00")  # such format 2021-05-15_04-20
    finish = request.GET.get("f", "9999-12-31_23-59")
    try:
        start = datetime.strptime(start, "%Y-%m-%d_%H-%M")
        finish = datetime.strptime(finish, "%Y-%m-%d_%H-%M")
    except ValueError:
        return Response(
            {"status": "wrong datetime format, try YYYY-MM-DD_hh-mm"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if units not in ("celsius", "fahrenheit"):
        return Response(
            {"status": "wrong temperature units, try 'celsius' or 'fahrenheit'"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    city_forecast = get_city_forecasts(city, units, start, finish)

    try:
        serializer = ForecastSerializer(city_forecast)
        return Response(serializer.data)
    except KeyError:
        return Response(
            {"status": "cant find that city"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def largest_cities_weather(request) -> Response:
    """Largest cities forecasts."""
    cities_list = get_largest_cities_toponyms(100)
    units = request.GET.get("u", "celsius")
    start = request.GET.get("s", "0001-01-01_00-00")  # such format 2021-05-15_04-20
    finish = request.GET.get("f", "9999-12-31_23-59")

    try:
        start = datetime.strptime(start, "%Y-%m-%d_%H-%M")
        finish = datetime.strptime(finish, "%Y-%m-%d_%H-%M")
    except ValueError:
        return Response(
            {"status": "wrong datetime format, try YYYY-MM-DD_hh-mm"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if units not in ("celsius", "fahrenheit"):
        return Response(
            {"status": "temperature units, try 'celsius' or 'fahrenheit'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cities_forecasts = get_cities_forecasts(cities_list, units, start, finish)

    try:
        serializer = ForecastSerializer(cities_forecasts, many=True)
        return Response(serializer.data)
    except KeyError:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def largest_cities_weather_download(request) -> HttpResponse:
    """Download largest cities forecasts"""
    cities_list = get_largest_cities_toponyms(100)
    units = request.GET.get("u", "celsius")
    start = request.GET.get("s", "0001-01-01_00-00")  # such format 2021-05-15_04-20
    finish = request.GET.get("f", "9999-12-31_23-59")

    try:
        start = datetime.strptime(start, "%Y-%m-%d_%H-%M")
        finish = datetime.strptime(finish, "%Y-%m-%d_%H-%M")
    except ValueError:
        return Response(
            {"status": "wrong datetime format, try YYYY-MM-DD_hh-mm"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if units not in ("celsius", "fahrenheit"):
        return Response(
            {"status": "temperature units, try 'celsius' or 'fahrenheit'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cities_forecasts = get_cities_forecasts(cities_list, units, start, finish)
    header = ["reception_time", "location", "units", "forecasts"]

    return write_to_csv(cities_forecasts, header)


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
