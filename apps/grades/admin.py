from django.contrib import admin

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import Course, GradeType, Lesson, CourseReview, AttendanceType, LessonDay
from apps.subscriptions.models import LessonBooking


class GradeTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(GradeType, GradeTypeAdmin)


class CourseReviewInline(admin.TabularInline):
    model = CourseReview
    extra = 0


class LessonDayInline(admin.TabularInline):
    model = LessonDay
    extra = 0


class CourceAdmin(admin.ModelAdmin):
    inlines = [LessonDayInline, CourseReviewInline]


admin.site.register(Course, CourceAdmin)


class LessonBookingInline(admin.TabularInline):
    model = LessonBooking
    extra = 0


class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonBookingInline]


admin.site.register(Lesson, LessonAdmin)


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(AttendanceType)
class AttendanceTypeAdmin(admin.ModelAdmin):
    pass
