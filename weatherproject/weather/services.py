import json
import os
from collections import namedtuple
from typing import Dict, List, Optional, Union

from pyowm.commons import exceptions
from pyowm.owm import OWM
from pyowm.weatherapi25.forecast import Forecast as ForecastOWM

API_KEY = os.getenv("API_KEY")  # Here's your API key from OpenWeatherMap


def get_city_forecaster(city: str) -> Optional[ForecastOWM]:
    """Function search for a city and return its forecast for the next 120 hours if it's found.
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
    except exceptions.NotFoundError:
        print("Unable to find the city.")
    except exceptions.InvalidSSLCertificateError:
        print("Wrong OWM API token.")
    except exceptions.APIRequestError:
        print("Network failure.")
    except exceptions.UnauthorizedError:
        print("OWM subscription insufficient capabilities.")
    finally:
        print(city_forecaster)
        return city_forecaster


def degrees_to_cardinal(deg: int) -> Optional[str]:
    """Function converts wind direction in angles to its text representation.
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


Weather = namedtuple(
    "Weather",
    [
        "time",
        "status",
        "temperature",
        "pressure",
        "wind_speed",
        "direction",
        "humidity",
        "rain",
        "snow",
    ],
)

Forecast = namedtuple(
    "Forecast",
    ["reception_time", "name", "coordinates", "ID", "country", "units", "forecasts"],
)


def parse_city_forecaster(
    forecast: ForecastOWM, units: str = "celsius"
) -> Union[Forecast, dict]:
    """Function parse forecast of the city if it's found and return Forecast namedtuple with forecasts.
    Args:
        forecast: The location's Forecast object.
        units: Temperature unit. Celsius and Fahrenheit are allowed. Defaults to Celsius.
    Returns:
        Return dictionary with forecasts of the place. If Forecast is None, return empty dictionary.
    """
    if forecast is None:
        return {}

    reception_time = dict(reception_time=forecast.reception_time("iso"))
    location = forecast.location.to_dict()

    forecasts = []
    for weather in forecast.weathers:
        reference_time = weather.reference_time("iso")
        weather_status = weather.detailed_status
        temperature = weather.temperature(units).get("temp", None)
        pressure = weather.pressure.get("press", None)
        wind = weather.wind()
        wind_speed = wind.get("speed")
        wind_direction = degrees_to_cardinal(wind.get("deg", None))
        humidity = weather.humidity
        rain = weather.rain.get("3h", 0)
        snow = weather.snow.get("3h", 0)
        forecasts.append(
            Weather(
                reference_time,
                weather_status,
                temperature,
                pressure,
                wind_speed,
                wind_direction,
                humidity,
                rain,
                snow,
            )._asdict()
        )
    return Forecast(
        **reception_time, **location, units=units, forecasts=forecasts
    )._asdict()  # TODO: remove _asdict
