from celery import shared_task
from django.conf import settings
from django.core.cache import cache

from .services import get_city_forecasts, get_largest_cities_toponyms


@shared_task
def cache_cities_forecasts(cities_num: int = 100) -> None:
    """Caching list of forecasts for the n-largest cities.

    Args:
        cities_num: num of largest cities.

    Returns:
        Cache list of forecasts for the given cities.
    """
    cities_forecasts = []

    cities_list = get_largest_cities_toponyms(cities_num)

    for city in cities_list:
        cities_forecasts.append(get_city_forecasts(city))

    cache.set("cities_forecasts", cities_forecasts, timeout=settings.CACHE_CITIES_TTL)
