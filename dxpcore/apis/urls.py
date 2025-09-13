from django.urls import path

from . import views

app_name = 'apis'

# ping api endpoint
urlpatterns = [
    path('', views.PingAPI.as_view(), name='ping'),
]

# dashboard - mobile app
urlpatterns += [
    path('dashboard/', views.DashboardDataAPI.as_view(), name='dashboard'),
    path('webdashboard/', views.WebDashboardDataAPI.as_view(), name='webdashboard'),
]

# accounts
urlpatterns += [
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('verifyotp/', views.VerifyOTPAPI.as_view(), name='verifyotp'),
    path('register/', views.RegisterUserAPI.as_view(), name='register'),
    path('users/', views.UsersListAPIView.as_view(), name='users'),
    path('userprofile/', views.UserProfileAPIView.as_view(), name='userprofile'),
    path('changepassword/', views.ChangePasswordAPIView.as_view(), name='changepassword'),
    path('resetpassword/', views.ResetPasswordAPIView.as_view(), name='resetpassword'),
    path('userpreferences/', views.UserPreferenceAPIView.as_view(), name='userpreferences'),
    path('accountdeletion/', views.AccountDeletionRequestAPIView.as_view(), name='accdel'),
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

# blog posts
urlpatterns += [
    path('blogs/', views.BlogsListAPI.as_view(), name='blogs'),
    path('readblog/', views.ViewBlogAPI.as_view(), name='readblog'),
]

# notifications
urlpatterns += [
    path('notifications/', views.NotificationsListAPI.as_view(), name='notifications'),
]

# chats, friend requests
urlpatterns += [
    path('people/', views.PeopleListAPIView.as_view(), name='people'),
    path('friendrequests/', views.FriendRequestsAPIView.as_view(), name='friendrequests'),
    path('sendfriendrequest/', views.SendFriendRequestAPIView.as_view(), name='sendfriendrequest'),
    path('acceptfriendrequest/', views.AcceptFriendRequestAPIView.as_view(), name='acceptfriendrequest'),
    path('rejectfriendrequest/', views.RejectFriendRequestAPIView.as_view(), name='rejectfriendrequest'),
    path('blockuser/', views.BlockUserAPIView.as_view(), name='blockuser'),
]