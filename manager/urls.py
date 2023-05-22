from django.urls import path 
from . import views
from .views import *

app_name = 'manager'

urlpatterns = [
        path('', views.manager_home, name='manager_home'),
        path('registrasi/', views.show_timregist, name='show_timregist'),
        path('detail/', views.show_teamdetail, name='show_teamdetail'),
        path('pemain/', views.show_addpemain, name='show_addpemain'),
        path('pelatih/', views.show_addpelatih, name='show_addpelatih'),
]