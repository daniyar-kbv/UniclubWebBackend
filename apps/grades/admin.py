from django.contrib import admin
from .models import Course, GradeType, Lesson, CourseReview, GradeTypeGroup, AttendanceType, LessonDay


class GradeTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(GradeType, GradeTypeAdmin)


class LessonDayInline(admin.StackedInline):
    model = LessonDay
    extra = 0


class CourceAdmin(admin.ModelAdmin):
    inlines = [LessonDayInline]


admin.site.register(Course, CourceAdmin)


class LessonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Lesson, LessonAdmin)


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(GradeTypeGroup)
class GradeTypeGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(AttendanceType)
class AttendanceTypeAdmin(admin.ModelAdmin):
    pass
