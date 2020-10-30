from django.contrib import admin

from .models import Subscription, FreezeRequest, LessonBooking

admin.site.register((FreezeRequest, Subscription))


@admin.register(LessonBooking)
class LessonBookingAdmin(admin.ModelAdmin):
    pass

