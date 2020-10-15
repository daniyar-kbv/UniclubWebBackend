from django.contrib import admin

from .models import Club, ClubImage, ClubReview


class ClubImageInline(admin.StackedInline):
    extra = 0
    model = ClubImage


class ClubAdmin(admin.ModelAdmin):
    inlines = ClubImageInline,
    readonly_fields = ['favorite_users']


admin.site.register(Club, ClubAdmin)


@admin.register(ClubReview)
class ClubReviewAdmin(admin.ModelAdmin):
    pass