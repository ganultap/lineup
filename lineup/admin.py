from django.contrib import admin
from .models import Session, Participant


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('screen_name', 'session', 'position', 'is_completed', 'added_at')
    list_filter = ('session', 'is_completed', 'added_at')
    search_fields = ('screen_name',)
    ordering = ('session', 'position')
