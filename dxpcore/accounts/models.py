'''
This module contains the models for the accounts application.
It includes the User, and OTP models.
These models are used to store information about the users 
and their otp information.

'''

from datetime import timedelta
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from dxpcore.utils.services import send_mail

from .manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    '''Custom User model for the application'''
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(default='Hello, I am using the Destination Experience App.', blank=True, null=True)

    deleted = models.BooleanField(default=False)  # Soft delete
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_from_app = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    # preferences
    preferred_notification_email = models.EmailField(max_length=50, blank=True, null=True)
    preferred_notification_phone = models.CharField(max_length=15, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'name']

    def __str__(self):
        return self.name

class OTP(models.Model):
    '''One Time Password model'''
    email = models.CharField(max_length=100)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self) -> bool:
        '''Returns True if the OTP is expired'''
        return (self.created_at + timedelta(minutes=30)) < timezone.now()
    
    def send_otp_to_user(self) -> None:
        '''Send the OTP to the user'''
        msg = f'Welcome to the Destination Experience App.\n\nYour OTP is {self.otp}\n\nRegards,\nDXP Team'
        send_mail([self.email], 'OTP', msg)

    def __str__(self):
        return self.email + ' - ' + self.otp