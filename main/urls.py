from django.urls import path
from .views import *

urlpatterns = [
    path('',index, name='home'),
    path('logout',custom_logout, name='logout'),
]