from django.contrib import admin

from .models import Account

# Custom account model registration
admin.site.register(Account)
