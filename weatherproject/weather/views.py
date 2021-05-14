from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from .services import *


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Simplest AF weather service</h1>")


def city_weather(request: HttpRequest, city: str) -> JsonResponse:
    """Return info about given city
    Args:
        request: Http request from user.
        city: City toponym in latin.
    Returns:
        JSON representation of forecast
    """
    city_forecaster = get_city_forecaster(city)
    city_forecast = parse_city_forecaster(city_forecaster)
    # return HttpResponse(json.dumps(city_forecast._asdict()))
    return JsonResponse(city_forecast, safe=False, json_dumps_params={"indent": 4})
