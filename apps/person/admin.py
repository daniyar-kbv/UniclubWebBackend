from django.contrib import admin

from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from .models import ClientProfile, ClientChildren
from apps.grades.models import Coach
from apps.subscriptions.models import Subscription, FreezeRequest, LessonBooking


class FreezeRequestInline(NestedStackedInline):
    model = FreezeRequest
    extra = 0


class SubscriptionInline(NestedStackedInline):
    model = Subscription
    extra = 0
    readonly_fields = ['id']
    inlines = [FreezeRequestInline]


class LessonBookingInline(NestedTabularInline):
    model = LessonBooking
    extra = 0
    raw_id_fields = ['lesson']


class ChildrenInline(NestedStackedInline):
    model = ClientChildren
    extra = 0
    inlines = [LessonBookingInline]


@admin.register(ClientProfile)
class ClientProfile(NestedModelAdmin):
    inlines = [ChildrenInline]


@admin.register(Coach)
class CoachProfile(admin.ModelAdmin):
    pass


@admin.register(ClientChildren)
class ClientChildrenAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'middle_name', 'email', 'mobile_phone']
