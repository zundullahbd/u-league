from django.urls import path 
from . import views
from .views import *

app_name = 'panitia'

urlpatterns = [
        path('', views.panitia_home, name='panitia_home'),
]