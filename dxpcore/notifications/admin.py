from django.contrib import admin

from .models import FCMDevice


@admin.register(FCMDevice)
class FCMDeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__name', 'token', 'created_at')
    search_fields = ('user__name', 'token')