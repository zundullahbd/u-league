from django.urls import path 
from . import views
from .views import *

app_name = 'authentication'

urlpatterns = [
      path('register/', views.register_form, name='register'),
      path('login/', login, name='login'),
      path('logout/', logout, name='logout'),
      path('', views.homepage, name='homepage'),
      path('register/register-manager', views.register_manager, name='register-manager'),
      path('register/register-panitia', views.register_panitia, name='register-panitia'),
      path('register/register-penonton', views.register_penonton, name='register-penonton'),
]
