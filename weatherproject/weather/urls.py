from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

# fmt: off
from .views.views_authentication import index, registration
from .views.views_forecast import (city_weather, largest_cities_weather,
                                   largest_cities_weather_download)

# fmt: on

app_name = "weather"

urlpatterns = [
    path("", index),
    path("register", registration),
    path("login", obtain_auth_token),
    path("cities/", largest_cities_weather),
    path("cities/download/", largest_cities_weather_download),
    path("weather/<str:city>/", city_weather),
]
