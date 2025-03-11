'''
This module contains the models for the accounts application.
It includes the User, and OTP models.
These models are used to store information about the users 
and their otp information.

'''

from datetime import timedelta, timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    '''Custom User model for the application'''
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    deleted = models.BooleanField(default=False)  # Soft delete
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

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

    def __str__(self):
        return self.email + ' - ' + self.otp