from django.contrib.auth.models import User
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from .services import *


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Simplest AF weather service</h1>")


def city_weather(request: HttpRequest, city: str) -> HttpResponse:
    """Return forecast about given city.
    Args:
        request: Http request from user.
        city: City toponym in latin.
    Returns:
        HttpResponse with forecast
    """
    city_forecaster = get_city_forecaster(city)
    units = request.GET.get("u", "celsius")
    city_forecast = parse_city_forecasts(city_forecaster, units)
    return HttpResponse(city_forecast)
    # return JsonResponse(
    #     model_to_dict(city_forecast), safe=False, json_dumps_params={"indent": 4}
    # )


def largest_cities_weather(request: HttpRequest) -> HttpResponse:
    """Return forecasts of the largest cities.

    Args:
        request: Http request from user.

    Returns:
        HttpResponse with forecasts
    """
    cities_list = get_largest_cities_toponyms(100)
    units = request.GET.get("u", "celsius")
    cities_forecasts = []
    for city in cities_list:
        city_forecaster = get_city_forecaster(city)
        cities_forecasts.append(parse_city_forecasts(city_forecaster, units))
    return HttpResponse(cities_forecasts)


def csv_download(request: HttpRequest) -> HttpResponse:
    """Download .csv file with largest cities forecasts.

    Args:
        request: Http request from user.

    Returns:
        Http response with "text/csv"
    """
    #### !!COPYPASTE FROM FUNC ABOVE. TEMPORARY!! ####
    cities_list = get_largest_cities_toponyms(100)
    units = request.GET.get("u", "celsius")
    cities_forecasts = []
    for city in cities_list:
        city_forecaster = get_city_forecaster(city)
        cities_forecasts.append(parse_city_forecasts(city_forecaster, units))
    #### !!COPYPASTE FROM FUNC ABOVE. TEMPORARY!! ####

    response = HttpResponse(content_type="text/csv")
    csv_tms = datetime.datetime.now().strftime(
        "%Y-%m-%d_%H-%M"
    )  # Timestamp for a file name, ex.: 2021-05-15_04-20
    response["Content-Disposition"] = f"attachment; filename=cities_{csv_tms}.csv"

    writer = csv.writer(response, delimiter=",")
    writer.writerow(["reception_time", "location", "units", "forecasts"])  # .csv header

    for city in cities_forecasts:
        writer.writerow(
            [city.reception_time, city.location, city.units, city.forecasts]
        )

    return response


def create_user(request: HttpRequest) -> JsonResponse:
    """Creates new user.

    Args:
        request: Http request from user

    Returns:
        Returns "Success!" if user is created, "Error!" otherwise.
    """
    # TODO: find out where to place all that crap (or leave it here in view.py)

    status = {"status": "Error!"}

    username = request.GET.get("u", None)
    password = request.GET.get("p", None)

    if None in (username, password):  # If query params are wrong.
        status["status"] += " Wrong query parameters"
        return JsonResponse(status)

    try:
        user = User.objects.create_user(username=username, password=password)
        if user is not None:
            status["status"] = "User has been created!"
    except IntegrityError:
        status["status"] += " User is already created."
    finally:
        return JsonResponse(status)
