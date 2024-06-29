from django.urls import path
from .views import *

urlpatterns = [
    path('login',login, name='login'),
    path('register',register, name='register'),
    path('activate/<str:token>/', activate_email, name='activate-account'),
    path('profile',profile, name = 'profile'),
    path('upload-profile-image/',update_profile, name='upload_dp'),
]