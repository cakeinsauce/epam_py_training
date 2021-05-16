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
def api_index(request) -> Response:
    """Index page API."""
    return Response({"message": "Simple as fukkk API weather service"})


@api_view(
    [
        "GET",
    ]
)
def api_city_weather(request, city: str) -> Response:
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


@api_view(
    [
        "GET",
    ]
)
def api_largest_cities_weather(request) -> Response:
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


@api_view(
    [
        "GET",
    ]
)
def api_largest_cities_weather_download(request) -> HttpResponse:
    """Download largest cities forecasts"""
    cities_list = get_largest_cities_toponyms(100)
    units = request.GET.get("u", "celsius")
    start = request.GET.get("s", datetime.min)  # such format 2021-05-15_04-20
    finish = request.GET.get("f", datetime.max)

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
