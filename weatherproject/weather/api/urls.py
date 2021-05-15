from django.urls import path

from .views import api_city_weather

app_name = "weather"

urlpatterns = [path("<city>/", api_city_weather)]
