import csv
import io
import os
import zipfile
from datetime import datetime
from typing import List, Optional, Tuple

import requests
from dateutil import parser
from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError
from django.http import HttpResponse
from pyowm.commons import exceptions as excOWM
from pyowm.owm import OWM
from pyowm.weatherapi25.forecast import Forecast as ForecastOWM

from .models import Forecast, Weather


def get_city_forecaster(city: str) -> Optional[ForecastOWM]:
    """Search for a city and return its forecast object for the next 120 hours.
    Args:
        city: The location's toponym. Add comma and 2-letter country code (ISO3166) to make it more precise.
    Returns:
        Return ForecastOWM object if city's found, None otherwise.
    """
    owm = OWM(settings.API_KEY)
    mgr = owm.weather_manager()
    city_forecaster = None

    if city in cache:  # Check if it's in cache
        return get_from_cache(city)

    try:
        city_forecaster = mgr.forecast_at_place(city, "3h").forecast
        cache.set(city, city_forecaster, timeout=settings.CACHE_TTL)
    except excOWM.InvalidSSLCertificateError:
        print("Wrong OWM API token.")
    except excOWM.APIRequestError:
        print("Network failure.")
    except excOWM.UnauthorizedError:
        print("OWM subscription insufficient capabilities.")
    except excOWM.NotFoundError:
        print("Unable to find the city.")
    finally:
        return city_forecaster


def degrees_to_cardinal(deg: int) -> Optional[str]:
    """Converts wind direction in angles to its text representation.
    Args:
        deg: Angular representation of wind direction.
    Returns:
        Return corresponding direction in text repr if it's there, None otherwise
    """
    if not str(deg).isnumeric():
        return None

    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    val = round(int(deg) / 45)
    return directions[val % 8]


def parse_city_forecasts(
    forecast: ForecastOWM, units: str = "celsius"
) -> Tuple[Forecast, List[Weather]]:
    """Parse ForecastOWM of the city if it's found and return List of Forecast with forecasts.
    Args:
        forecast: The location's ForecastOWM object.
        units: Temperature unit. Celsius and Fahrenheit are allowed. Defaults to Celsius.

    Returns:
        Return Forecast instance with forecasts of the place within a given period.
        If ForecastOWM is None, return empty dictionary.
    """
    if forecast is None:
        return []

    reception_time = parser.parse(forecast.reception_time("iso"))
    location = forecast.location.to_dict()
    city_forecasts = []

    for weather in forecast.weathers:
        reference_time = parser.parse(weather.reference_time("iso"), ignoretz=False)
        weather_status = weather.detailed_status
        temperature = weather.temperature(units).get("temp", None)
        pressure = weather.pressure.get("press", None)
        wind = weather.wind()
        wind_speed = wind.get("speed", None)
        wind_direction = degrees_to_cardinal(wind.get("deg", None))
        humidity = weather.humidity
        rain = weather.rain.get("3h", 0)
        snow = weather.snow.get("3h", 0)

        weather_model = Weather(
            time=reference_time,
            status=weather_status,
            temperature=temperature,
            pressure=pressure,
            wind_speed=wind_speed,
            direction=wind_direction,
            humidity=humidity,
            rain=rain,
            snow=snow,
        )

        city_forecasts.append(weather_model)

    forecast_model = Forecast(
        reception_time=reception_time, location=location, unit=units
    )

    return forecast_model, city_forecasts


def get_city_forecasts(
    city: str,
    units: str = "celsius",
) -> Tuple[Forecast, List[Weather]]:
    """Get city forecast.

    Args:
        city: City's toponym.
        units: Temperature unit

    Returns:
        Forecast of the city
    """
    city_forecaster = get_city_forecaster(city)
    return parse_city_forecasts(city_forecaster, units)


def save_city_forecasts_to_db(city_forecasts: List[Weather]) -> List[Weather]:
    """Saves city forecasts to db, helps with ManyToMany field."""
    forecasts = []
    for weather in city_forecasts:
        try:
            weather.save()
            forecasts.append(weather)
        except IntegrityError:
            pass
    return forecasts


def get_from_cache(key_name: str):
    """Get value from cache."""
    return cache.get(key_name)


def get_cities_forecasts_for_period(
    cities_forecasts: List[Forecast],
    datetime_start: datetime,
    datetime_finish: datetime,
    units: str = "celsius",
) -> List[Forecast]:
    """Get list of forecasts for the given cities within period.

    Args:
        cities_forecasts: List of forecasts to be processed.
        datetime_start: Forecast datetime start.
        datetime_finish: Forecast datetime finish.
        units: Temperature unit. Celsius and Fahrenheit are allowed. Defaults to Celsius.

    Returns:
        List of cities' forecasts within given period in given temperature unit.

    Raises:
        RuntimeError: If cities' forecasts are None.

    """
    fahrenheit = False

    if cities_forecasts is None:
        raise RuntimeError

    if units == "fahrenheit":
        fahrenheit = True

    forecasts = []

    for city in cities_forecasts:
        city_forecasts = []
        for forecast in city.forecasts:
            if (
                datetime_start <= forecast["time"] <= datetime_finish
            ):  # If forecast within of the given time period.
                if fahrenheit:  # Celsius to Fahrenheit.
                    forecast["temperature"] = round(
                        forecast["temperature"] * 9 / 5 + 32, 1
                    )
                city_forecasts.append(forecast)
        city.units = units
        city.forecasts = city_forecasts
        forecasts.append(city)
    return forecasts


def write_to_csv(cities_forecasts: List[Forecast]) -> HttpResponse:
    """Write List of Forecasts to HttpResponse text/csv.

    Args:
        cities_forecasts: List of Forecast.

    Returns:
        Http response with .csv file of forecasts.
    """
    header = ["reception_time", "location", "units", "forecasts"]

    csv_tms = datetime.now().strftime(
        "%Y-%m-%d_%H-%M"
    )  # Timestamp for a file name, ex.: 2021-05-15_04-20

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename=cities_{csv_tms}.csv"
    writer = csv.writer(response, delimiter=",")
    writer.writerow(header)

    for city in cities_forecasts:
        writer.writerow([city.reception_time, city.location, city.unit, city.forecast])

    return response


def get_largest_cities_toponyms(
    cities_amount: int = 100, csv_name: str = "worldcities.csv"
) -> List[str]:
    """Extract most populated cities toponyms from .csv file inside of a .zip.

    Args:
        cities_amount: Amount of largest cities to extract. Defaults to 100.
        csv_name: csv-file name. Defaults to "worldcities.csv"

    Returns:
        List of n largest cities in descending order.
    """
    url = "https://simplemaps.com/static/data/world-cities/basic/simplemaps_worldcities_basicv1.73.zip"

    with requests.get(
        url, allow_redirects=True
    ) as request:  # Download .zip with .csv data.
        with open("cities.zip", "wb") as writer:
            writer.write(request.content)

    with zipfile.ZipFile("cities.zip") as archive:  # Extract .csv file from .zip
        archive.extract(csv_name)

    with io.open(csv_name, encoding="utf-8", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        reader.__next__()  # Skip header of csv.
        largest_cities_toponyms = [reader.__next__()[1] for _ in range(cities_amount)]

    os.remove(csv_name)
    os.remove("cities.zip")

    return largest_cities_toponyms
