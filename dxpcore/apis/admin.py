from django.contrib import admin

from .models import Blog, ChatRoom, FriendRequest, Hotel, Political, TouristSite, Message


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

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'is_published', 'created_at')
    search_fields = ('title', 'writer__name')
    list_filter = ('is_published', 'created_at')


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'created_at')
    search_fields = ('sender__name', 'receiver__name')
    list_filter = ('created_at',)

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_id', 'name', 'is_group', 'created_at')
    search_fields = ('room_id', 'name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'sender', 'content', 'timestamp')
    search_fields = ('room__name', 'sender__name', 'content')
    list_filter = ('timestamp',)