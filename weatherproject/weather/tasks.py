from celery import shared_task

# fmt: off
from .services import (get_city_forecasts, get_largest_cities_toponyms,
                       save_city_forecasts_to_db)

# fmt: on


@shared_task
def save_cities_forecasts(cities_num: int = 100) -> None:
    """Caching list of forecasts for the n-largest cities.

    Args:
        cities_num: num of largest cities.

    Returns:
        Cache list of forecasts for the given cities.
    """
    cities_list = get_largest_cities_toponyms(cities_num)

    for city in cities_list:
        city_data = get_city_forecasts(city)
        city_info = city_data[0]  # City info
        city_forecasts = city_data[1]  # City forecasts

        city_info.save()
        city_info.forecasts.add(*save_city_forecasts_to_db(city_forecasts))
