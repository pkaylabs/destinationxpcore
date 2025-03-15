from django.urls import path

from . import views

app_name = 'apis'

# ping api endpoint
urlpatterns = [
    path('', views.PingAPI.as_view(), name='ping'),
]   

# accounts
urlpatterns += [
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('register/', views.RegisterUserAPI.as_view(), name='register'),
    path('users/', views.UsersListAPIView.as_view(), name='users'),
    path('userprofile/', views.UserProfileAPIView.as_view(), name='userprofile'),
]

# hotels
urlpatterns += [
    path('hotels/', views.HotelListAPI.as_view(), name='hotels'),
]

# political sites
urlpatterns += [
    path('political/', views.PoliticalListAPI.as_view(), name='political'),
]

# tourist sites
urlpatterns += [
    path('tourists/', views.TouristSiteListAPI.as_view(), name='tourists'),
]