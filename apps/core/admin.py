from django.contrib import admin

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import CityModel, GradeTypeGroup, GradeType, AdministrativeDivision


class GradeTypeInline(admin.StackedInline):
    model = GradeType
    extra = 0


@admin.register(GradeTypeGroup)
class GradeTypeGroupAdmin(admin.ModelAdmin):
    inlines = [GradeTypeInline]


class HiddenAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}  # Hide model in admin list


class ChangeOnlyMixin:
    def has_add_permission(self, request, obj=None):
        return False


class ReadOnlyMixin(ChangeOnlyMixin):
    def has_change_permission(self, request, obj=None):
        return False


class AdministrativeDivisionInline(admin.TabularInline):
    model = AdministrativeDivision
    extra = 0


@admin.register(CityModel)
class CityModelAdmin(admin.ModelAdmin):
    inlines = [AdministrativeDivisionInline]
