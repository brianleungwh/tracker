from django.contrib import admin
from api.models import User, Tracker

class TrackerInline(admin.TabularInline):
    model = Tracker


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', )

    inlines = [
        TrackerInline,
    ]


class TrackerAdmin(admin.ModelAdmin):
    list_display = ('results_page_url', )

    def User(self, obj):
        return obj.email


admin.site.register(User, UserAdmin)
admin.site.register(Tracker, TrackerAdmin)
