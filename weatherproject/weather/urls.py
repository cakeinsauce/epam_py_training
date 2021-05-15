from django.urls import path

from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("register/", create_user, name="register"),
    path("cities/", largest_cities_weather, name="cities"),
    path("cities/csv", csv_download, name="csv_download"),
    path("<str:city>/", city_weather, name="weather"),
]
