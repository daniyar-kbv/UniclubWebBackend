from django.contrib import admin

from .models import Subscription, FreezeRequest, LessonBooking, SubscriptionHistoryRecord


class FreezeRequestInline(admin.TabularInline):
    model = FreezeRequest
    extra = 0


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [FreezeRequestInline]


@admin.register(LessonBooking)
class LessonBookingAdmin(admin.ModelAdmin):
    pass


@admin.register(SubscriptionHistoryRecord)
class SubscriptionHistoryRecord(admin.ModelAdmin):
    pass

