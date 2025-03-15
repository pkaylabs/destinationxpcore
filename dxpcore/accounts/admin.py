from django.contrib import admin

from .models import *

admin.site.site_header = 'DESTINATION XP Portal'

# user
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id' ,'name', 'email', 'phone', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('name', 'email', 'phone',)

