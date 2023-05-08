from django.urls import path 
from . import views
from .views import *

app_name = 'penonton'

urlpatterns = [
        path('', views.penonton_home, name='penonton_home'),
]