from django.contrib import admin

from .models import Club, ClubImage


class ClubImageInline(admin.StackedInline):
    extra = 0
    model = ClubImage


class ClubAdmin(admin.ModelAdmin):
    inlines = ClubImageInline,


admin.site.register(Club, ClubAdmin)
