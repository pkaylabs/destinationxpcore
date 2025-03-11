from django.db import models

from dxpcore.utils.constants import HotelCategory
from dxpcore.utils.constants import PoliticalCategory
from dxpcore.utils.constants import TourismCategory


class Hotel(models.Model):
    '''Model to store information about hotels'''
    categories = (
        (HotelCategory.STANDARD.name, HotelCategory.STANDARD.value),
        (HotelCategory.SHORTSTAY.name, HotelCategory.SHORTSTAY.value),
        (HotelCategory.FAMILY.name, HotelCategory.FAMILY.value),
        (HotelCategory.BOOTIQUE.name, HotelCategory.BOOTIQUE.value),
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    website = models.URLField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='hotels/')
    second_image = models.ImageField(upload_to='hotels/', null=True, blank=True)
    third_image = models.ImageField(upload_to='hotels/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=categories) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Political(models.Model):
    '''Model to store information about political sites'''
    categories = (
        (PoliticalCategory.MINISTRY.name, PoliticalCategory.MINISTRY.value),
        (PoliticalCategory.DEPARTMENT.name, PoliticalCategory.DEPARTMENT.value),
        (PoliticalCategory.AGENCY.name, PoliticalCategory.AGENCY.value),
        (PoliticalCategory.OTHERS.name, PoliticalCategory.OTHERS.value),
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    landmark = models.CharField(max_length=255)
    custodian = models.URLField(max_length=200)
    category = models.CharField(max_length=50, choices=categories)
    description = models.TextField()
    image = models.ImageField(upload_to='political/')
    second_image = models.ImageField(upload_to='political/', null=True, blank=True)
    third_image = models.ImageField(upload_to='political/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class TouristSite(models.Model):
    '''Model to store information about tourist sites'''
    categories = (
        (TourismCategory.HISTORICAL.name, TourismCategory.HISTORICAL.value),
        (TourismCategory.CULTURAL.name, TourismCategory.CULTURAL.value),
        (TourismCategory.LEISURE.name, TourismCategory.LEISURE.value),
        (TourismCategory.NATURE.name, TourismCategory.NATURE.value),
        (TourismCategory.ENTERTAINMENT.name, TourismCategory.ENTERTAINMENT.value),
        (TourismCategory.OTHERS.name, TourismCategory.OTHERS.value),
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    landmark = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='tourism/')
    second_image = models.ImageField(upload_to='tourism/', null=True, blank=True)
    third_image = models.ImageField(upload_to='tourism/', null=True, blank=True)
    category = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name