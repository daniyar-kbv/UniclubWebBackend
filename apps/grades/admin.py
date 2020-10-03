from django.contrib import admin
from .models import Grade, Course, GradeType


class GradeTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(GradeType, GradeTypeAdmin)


class GradeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Grade, GradeAdmin)


class CourceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourceAdmin)