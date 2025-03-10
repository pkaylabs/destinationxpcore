from django.urls import path

from .views import dashboard

app_name = 'apis'

# ping api endpoint
urlpatterns = [
    path('', dashboard.PingAPI.as_view(), name='ping'),
]   
