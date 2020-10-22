from django.contrib import admin

from .models import FAQ, PartnerFeedBack, FeedBack, BookingApplication

admin.site.register(FAQ)
admin.site.register(PartnerFeedBack)
admin.site.register(FeedBack)


@admin.register(BookingApplication)
class BookingApplicationModelAdmin(admin.ModelAdmin):
    filter_horizontal = ['lesson_days']
    readonly_fields = ['lesson_days']
