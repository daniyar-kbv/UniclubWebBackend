from django.contrib import admin

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from apps.grades.models import Coach, Course
from .models import Club, ClubImage, ClubReview


class CourseInline(admin.StackedInline):
    model = Course
    extra = 0


class CoachInline(admin.TabularInline):
    model = Coach
    extra = 0


class ClubReviewInline(admin.StackedInline):
    model = ClubReview
    extra = 0


class ClubImageInline(admin.TabularInline):
    extra = 0
    model = ClubImage


class ClubAdmin(admin.ModelAdmin):
    inlines = [ClubImageInline, CoachInline, CourseInline, ClubReviewInline]
    readonly_fields = ['favorite_users']


admin.site.register(Club, ClubAdmin)


@admin.register(ClubReview)
class ClubReviewAdmin(admin.ModelAdmin):
    pass