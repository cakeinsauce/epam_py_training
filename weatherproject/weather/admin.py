from django.contrib import admin

from .models import Account, Forecast, Weather

# Custom account model registration
admin.site.register(Account)
admin.site.register(Forecast)
admin.site.register(Weather)
