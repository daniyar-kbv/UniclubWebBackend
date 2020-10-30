from django.contrib import admin

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import Course, GradeType, Lesson, CourseReview, AttendanceType, LessonDay


class GradeTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(GradeType, GradeTypeAdmin)


class CourseReviewInline(admin.StackedInline):
    model = CourseReview
    extra = 0


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0
    raw_id_fields = ['lesson_day']


class LessonDayInline(admin.StackedInline):
    model = LessonDay
    extra = 0


class CourceAdmin(admin.ModelAdmin):
    inlines = [LessonDayInline, LessonInline, CourseReviewInline]


admin.site.register(Course, CourceAdmin)


class LessonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Lesson, LessonAdmin)


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(AttendanceType)
class AttendanceTypeAdmin(admin.ModelAdmin):
    pass
