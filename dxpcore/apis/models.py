from uuid import uuid4
from django.db import models
from django.conf import settings
from accounts.models import User
from dxpcore.utils.constants import (BlogCategory, HotelCategory, PoliticalCategory,
                                     TourismCategory)
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class ChatRoom(models.Model):
    '''The chatroom model for storing different chatrooms'''
    # user uuid for the room_id
    room_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=100, unique=True)
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_unread_messages(self, user):
        '''Returns the total number of unread messages for a user in this chatroom'''
        return self.messages.filter(is_read=False, sender__is_active=True).exclude(sender=user).count()
    
    def read_all_messages(self, user):
        '''Marks all messages as read for a user in this chatroom'''
        self.messages.filter(is_read=False, sender__is_active=True).exclude(sender=user).update(is_read=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    '''Messsage model for storing user messages'''
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.name}: {self.content[:20]}"


class FriendRequest(models.Model):
    '''Model to store friend requests between users'''
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.name} -> {self.receiver.name}"


class Hotel(models.Model):
    '''Model to store information about hotels'''
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    website = models.URLField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='hotels/', null=True, blank=True)
    second_image = models.ImageField(upload_to='hotels/', null=True, blank=True)
    third_image = models.ImageField(upload_to='hotels/', null=True, blank=True)
    category = models.CharField(max_length=50, default=HotelCategory.STANDARD.value) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Political(models.Model):
    '''Model to store information about political sites'''
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    landmark = models.CharField(max_length=255)
    custodian = models.CharField(max_length=200)
    category = models.CharField(max_length=50,default=PoliticalCategory.OTHERS.value)
    description = models.TextField()
    image = models.ImageField(upload_to='political/', null=True, blank=True)
    second_image = models.ImageField(upload_to='political/', null=True, blank=True)
    third_image = models.ImageField(upload_to='political/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class TouristSite(models.Model):
    '''Model to store information about tourist sites'''
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    landmark = models.CharField(max_length=255)
    custodian = models.CharField(max_length=200, default='No Custodian Identified')
    description = models.TextField()
    image = models.ImageField(upload_to='tourism/', null=True, blank=True)
    second_image = models.ImageField(upload_to='tourism/', null=True, blank=True)
    third_image = models.ImageField(upload_to='tourism/', null=True, blank=True)
    category = models.CharField(max_length=50, default=TourismCategory.OTHERS.value)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Blog(models.Model):
    '''Model to store blogs'''

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=250, default='')
    content = models.TextField()
    category = models.CharField(max_length=20, default=BlogCategory.TRAVEL.value)
    feature_image = models.ImageField(upload_to='blog/', null=True, blank=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def writer_name(self):
        '''Returns the name of the writer'''
        return self.writer.name if self.writer else None
    
    @property
    def writer_image(self):
        '''Returns the image of the writer'''
        return self.writer.avatar.url if self.writer and self.writer.avatar else ''

    def __str__(self):
        return self.title


class BlogView(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user or self.ip_address} viewed {self.blog.title} at {self.created_at}"


class Notification(models.Model):
    '''Model to store notifications for users'''
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)

    def __str__(self):
        return f'Notification: {self.title}'

@receiver(post_save, sender=ChatRoom)
def broadcast_chatroom_update(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chatrooms_updates',
            {'type': 'chatrooms_update'}
        )