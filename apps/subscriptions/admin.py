from django.contrib import admin

from .models import Subscription, FreezeRequest

admin.site.register((FreezeRequest, Subscription))
