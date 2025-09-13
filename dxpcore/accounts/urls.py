
from django.urls import path
from . import views

urlpatterns = [
    path('eula/', views.EULAView.as_view(), name='eula'),
]
