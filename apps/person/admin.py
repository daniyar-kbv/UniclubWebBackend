from django.contrib import admin

from .models import ClientProfile, ClientChildren
from apps.grades.models import Coach
from apps.subscriptions.models import Subscription


class ChildrenInline(admin.StackedInline):
    model = ClientChildren
    extra = 0


@admin.register(ClientProfile)
class ClientProfile(admin.ModelAdmin):
    inlines = [ChildrenInline]


@admin.register(Coach)
class CoachProfile(admin.ModelAdmin):
    pass


class ChildSubscriptionInline(admin.StackedInline):
    model = Subscription
    extra = 0


@admin.register(ClientChildren)
class ClientChildrenAdmin(admin.ModelAdmin):
    inlines = [ChildSubscriptionInline]
