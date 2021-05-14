from django.urls import path

from .views import *

urlpatterns = [
    path("", index),
    path("<str:city>/", city_weather),
]
