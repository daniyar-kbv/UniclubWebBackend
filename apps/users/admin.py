from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django import forms

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from apps.person.models import ClientProfile, ClientChildren
from apps.clubs.models import Club
from apps.subscriptions.models import Subscription
from . import UserTypes

User = get_user_model()


class SubscriptionInline(NestedStackedInline):
    model = Subscription
    extra = 0


class ClubInline(NestedStackedInline):
    model = Club


class ProfileInline(NestedStackedInline):
    model = ClientProfile


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('mobile_phone', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'middle_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Type'), {'fields': ('user_type',)}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_phone', 'password1', 'password2', 'user_type'),
        }),
    )
    list_display = ('mobile_phone', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'mobile_phone')
    ordering = ()
    filter_horizontal = ()
    inlines = [ClubInline, ProfileInline, SubscriptionInline]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if obj:
                if inline.__class__ == ProfileInline or \
                        inline.__class__ == ClubInline or  \
                        inline.__class__ == SubscriptionInline:
                    if obj.user_type == UserTypes.CLIENT and (inline.__class__ == ProfileInline or
                                                              inline.__class__ == SubscriptionInline):
                        yield inline.get_formset(request, obj), inline
                    elif obj.user_type == UserTypes.PARTNER and inline.__class__ == ClubInline:
                        yield inline.get_formset(request, obj), inline
                else:
                    yield inline.get_formset(request, obj), inline


admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
