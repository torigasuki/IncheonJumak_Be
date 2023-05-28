from django.contrib import admin
from information.models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ['eventname', 'region', 'started_at', 'ended_at', 'alchol']
    list_display_links = ['eventname',]

    list_filter = ('started_at', 'ended_at')

    fieldsets = (
        (None, {
            'fields': ('eventname', 'image', 'region', 'alchol')
        }),
        ('Period', {
            'fields': ('started_at', 'ended_at')
        }),
    )

admin.site.register(Event, EventAdmin)
