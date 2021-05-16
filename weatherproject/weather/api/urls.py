from django.urls import path

# fmt: off
from .views import *

# fmt: on

app_name = "weather"

urlpatterns = [
    path("", api_index),
    path("register", api_registration),
    path("cities/", api_largest_cities_weather),
    path("cities/download/", api_largest_cities_weather_download),
    path("weather/<str:city>/", api_city_weather),
]
