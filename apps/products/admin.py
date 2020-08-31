from django.contrib import admin

from .models import Benefits, Product

admin.site.register((Benefits, Product))
