import csv
import io
import os
import zipfile
from datetime import datetime
from typing import List, Optional, Union

import requests
from dateutil import parser
from django.forms.models import model_to_dict
from django.http import HttpResponse
from pyowm.commons import exceptions as excOWM
from pyowm.owm import OWM
from pyowm.weatherapi25.forecast import Forecast as ForecastOWM

from .models import Forecast, Weather

API_KEY = os.getenv("API_KEY")  # Here's your API key from OpenWeatherMap


def get_city_forecaster(city: str) -> Optional[ForecastOWM]:
    """Search for a city and return its forecast object for the next 120.
    Args:
        city: The location's toponym. Add comma and 2-letter country code (ISO3166) to make it more precise.
    Returns:
        Return Forecast object if city's found, None otherwise.
    """
    owm = OWM(API_KEY)
    mgr = owm.weather_manager()
    city_forecaster = None

    try:
        city_forecaster = mgr.forecast_at_place(city, "3h").forecast
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
    forecast: ForecastOWM,
    units: str = "celsius",
    datetime_start: datetime = datetime.min,
    datetime_finish: datetime = datetime.max,
) -> Union[Forecast, dict]:
    """Parse ForecastOWM of the city if it's found and return Forecast with forecasts within a given period.
    Args:
        forecast: The location's Forecast object.
        units: Temperature unit. Celsius and Fahrenheit are allowed. Defaults to Celsius.
        datetime_start: Forecast datetime finish. If not given, consider as min time for forecast
        datetime_finish: Forecast datetime start. If not given, consider as max time for forecast
    Returns:
        Return Forecast instance with forecasts of the place within a given period. If ForecastOWM is None, return empty dictionary.
    """
    if forecast is None:
        return {}  # TODO: change that stupidity

    reception_time = parser.parse(forecast.reception_time("iso"))
    location = forecast.location.to_dict()

    forecasts = []

    for weather in forecast.weathers:
        reference_time = parser.parse(weather.reference_time("iso"), ignoretz=True)
        weather_status = weather.detailed_status
        temperature = weather.temperature(units).get("temp", None)
        pressure = weather.pressure.get("press", None)
        wind = weather.wind()
        wind_speed = wind.get("speed")
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

        if datetime_start <= reference_time <= datetime_finish:
            dict_weather = model_to_dict(weather_model)
            forecasts.append(dict_weather)

    forecast_model = Forecast(
        reception_time=reception_time,
        location=location,
        units=units,
        forecasts=forecasts,
    )
    return forecast_model


def get_largest_cities_toponyms(
    cities_amount: int = 100, csv_name: str = "worldcities.csv"
) -> List[str]:
    """Extract most populated cities toponyms from .csv file inside of a .zip.

    Args:
        cities_amount: Amount of largest cities to extract. Defaults to 100.
        csv_name: csv-file name. Defaults to "worldcities.csv"

    Returns:
        List of 100 largest cities in descending order.
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


def get_city_forecasts(
    city: str,
    units: str = "celsius",
    datetime_start: datetime = datetime.min,
    datetime_finish: datetime = datetime.max,
) -> Union[Forecast, dict]:
    """Get city forecast.

    Args:
        city: City's toponym.
        units: Temperature unit
        datetime_start: Forecast datetime finish. If not given, consider as min time for forecast
        datetime_finish: Forecast datetime start. If not given, consider as max time for forecast.

    Returns:
        Forecast of the city
    """
    city_forecaster = get_city_forecaster(city)
    return parse_city_forecasts(city_forecaster, units, datetime_start, datetime_finish)


def get_cities_forecasts(
    cities_list: List[str],
    units: str = "celsius",
    datetime_start: datetime = datetime.min,
    datetime_finish: datetime = datetime.max,
) -> List[Forecast]:
    """Get list of forecasts for the given cities.

    Args:
        units: Temperature unit. Celsius and Fahrenheit are allowed. Defaults to Celsius.
        cities_list: list of cities which forecasts are needed
        datetime_start: Forecast datetime finish. If not given, consider as min time for forecast
        datetime_finish: Forecast datetime start. If not given, consider as max time for forecast.
    Returns:
        Return list of forecasts for the given cities.
    """
    cities_forecasts = []
    for city in cities_list:
        cities_forecasts.append(
            get_city_forecasts(city, units, datetime_start, datetime_finish)
        )
    return cities_forecasts


def write_to_csv(cities_forecasts: List[Forecast], header: List[str]) -> HttpResponse:
    """Write Forecast to HttpResponse text/csv.

    Args:
        header: header of .csv file
        cities_forecasts: List of Forecast.

    Returns:
        Http response with .csv file of forecasts
    """
    csv_tms = datetime.now().strftime(
        "%Y-%m-%d_%H-%M"
    )  # Timestamp for a file name, ex.: 2021-05-15_04-20
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename=cities_{csv_tms}.csv"
    writer = csv.writer(response, delimiter=",")
    writer.writerow(header)  # .csv header

    for city in cities_forecasts:
        writer.writerow(
            [city.reception_time, city.location, city.units, city.forecasts]
        )
    return response
