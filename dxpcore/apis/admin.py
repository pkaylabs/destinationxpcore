from django.contrib import admin

from .models import Hotel, Political, TouristSite


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'website', 'created_at')
    search_fields = ('name', 'address')
    # list_filter = ('address', 'price', 'rating')

@admin.register(Political)
class PoliticalAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'landmark', 'created_at')
    search_fields = ('name', 'address')

@admin.register(TouristSite)
class TouristSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'landmark', 'created_at')
    search_fields = ('name', 'address')
