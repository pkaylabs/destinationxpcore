from django.db import models
from django.conf import settings
from accounts.models import User
from dxpcore.utils.constants import (BlogCategory, HotelCategory, PoliticalCategory,
                                     TourismCategory)




class ChatRoom(models.Model):
    '''The chatroom model for storing different chatrooms'''
    name = models.CharField(max_length=100, unique=True)
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    '''Messsage model for storing user messages'''
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

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


class Notification(models.Model):
    '''Model to store notifications for users'''
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)

    def __str__(self):
        return f'Notification: {self.title}'