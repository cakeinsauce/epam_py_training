from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

# fmt: off
from .views import (api_city_weather, api_index, api_largest_cities_weather,
                    api_largest_cities_weather_download, api_registration)

# fmt: on
app_name = "weather"

urlpatterns = [
    path("", api_index),
    path("register", api_registration),
    path("login", obtain_auth_token),
    path("cities/", api_largest_cities_weather),
    path("cities/download/", api_largest_cities_weather_download),
    path("weather/<str:city>/", api_city_weather),
]
