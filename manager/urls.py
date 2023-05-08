from django.urls import path 
from . import views
from .views import *

app_name = 'manager'

urlpatterns = [
        path('', views.manager_home, name='manager_home'),
]