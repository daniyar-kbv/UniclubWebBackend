from django.contrib import admin

from .models import ClientProfile
from apps.grades.models import Coach


@admin.register(ClientProfile)
class ClientProfile(admin.ModelAdmin):
    pass


@admin.register(Coach)
class CoachProfile(admin.ModelAdmin):
    pass
