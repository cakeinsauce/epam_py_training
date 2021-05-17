from datetime import datetime

from celery import shared_task
from django.conf import settings
from django.core.cache import cache

from .services import get_city_forecasts, get_largest_cities_toponyms


@shared_task
def cache_cities_forecasts(
    cities_num: int = 100,
    units: str = "celsius",
    datetime_start: datetime = datetime.min,
    datetime_finish: datetime = datetime.max,
) -> None:
    """Caching list of forecasts for the given cities.

    Args:
        cities_num: num of largest cities which forecasts are needed
        units: Temperature unit. Celsius and Fahrenheit are allowed. Defaults to Celsius.
        datetime_start: Forecast datetime finish. If not given, consider as min time for forecast
        datetime_finish: Forecast datetime start. If not given, consider as max time for forecast.
    Returns:
        Return list of forecasts for the given cities.
    """
    cities_forecasts = []

    cities_list = get_largest_cities_toponyms(cities_num)

    for city in cities_list:
        cities_forecasts.append(
            get_city_forecasts(city, units, datetime_start, datetime_finish)
        )

    cache.set("cities_forecasts", cities_forecasts, timeout=settings.CACHE_CITIES_TTL)


cache_cities_forecasts(100)
