from django.conf import settings
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import ForecastSerializer, RegistrationSerializer
from .services import *

# TODO: Find out what to do with query params validation and exceptions


@api_view(["GET"])
@permission_classes([AllowAny])
def index(request) -> Response:
    """Index page API."""
    return Response({"message": "Simple as fukkk API weather service"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@cache_page(settings.CACHE_TTL)
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
            {"message": "wrong datetime format, try YYYY-MM-DD_hh-mm"},
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
            {"message": "cant find that city"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@cache_page(settings.CACHE_TTL)
def largest_cities_weather_download(request) -> HttpResponse:
    """Download largest cities forecasts"""
    units = request.GET.get("u", "celsius")
    start = request.GET.get("s", "0001-01-01_00-00")  # such format 2021-05-15_04-20
    finish = request.GET.get("f", "9999-12-31_23-59")
    try:
        start = datetime.strptime(start, "%Y-%m-%d_%H-%M")
        finish = datetime.strptime(finish, "%Y-%m-%d_%H-%M")
    except ValueError:
        return Response(
            {"message": "wrong datetime format, try YYYY-MM-DD_hh-mm"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if units not in ("celsius", "fahrenheit"):
        return Response(
            {"message": "wrong temperature units, try 'celsius' or 'fahrenheit'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        cities_forecasts = get_cities_forecasts_from_cache_for_period(
            start, finish, units
        )
    except RuntimeError:  # Cities forecasts are not cached. Run celery and celery-beat!
        return HttpResponse(
            {"message": "cities data is not ready, try it later"}, status=404
        )

    return write_to_csv(cities_forecasts)


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


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def largest_cities_weather(request) -> Response:
#     """Largest cities forecasts."""
#     cities_num = 100
#     units = request.GET.get("u", "celsius")
#     start = request.GET.get("s", "0001-01-01_00-00")  # such format 2021-05-15_04-20
#     finish = request.GET.get("f", "9999-12-31_23-59")
#
#     try:
#         start = datetime.strptime(start, "%Y-%m-%d_%H-%M")
#         finish = datetime.strptime(finish, "%Y-%m-%d_%H-%M")
#     except ValueError:
#         return Response(
#             {"status": "wrong datetime format, try YYYY-MM-DD_hh-mm"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#
#     if units not in ("celsius", "fahrenheit"):
#         return Response(
#             {"status": "temperature units, try 'celsius' or 'fahrenheit'"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#
#     cities_forecasts = get_cities_forecasts(cities_num, units, start, finish)
#
#     try:
#         serializer = ForecastSerializer(cities_forecasts, many=True)
#         return Response(serializer.data)
#     except KeyError:
#         return Response(status=status.HTTP_404_NOT_FOUND)
