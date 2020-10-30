from django.contrib import admin

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from apps.grades.models import Coach, Course
from .models import Club, ClubImage, ClubReview


class CourseInline(NestedStackedInline):
    model = Course
    extra = 0


class CoachInline(NestedStackedInline):
    model = Coach
    extra = 0


class ClubReviewInline(NestedStackedInline):
    model = ClubReview
    extra = 0


class ClubImageInline(NestedStackedInline):
    extra = 0
    model = ClubImage


class ClubAdmin(NestedModelAdmin):
    inlines = [ClubImageInline, CoachInline, CourseInline, ClubReviewInline]
    readonly_fields = ['favorite_users']


admin.site.register(Club, ClubAdmin)


@admin.register(ClubReview)
class ClubReviewAdmin(admin.ModelAdmin):
    pass