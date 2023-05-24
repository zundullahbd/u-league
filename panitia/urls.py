from django.urls import path 
from . import views
from .views import *

app_name = 'panitia'

urlpatterns = [
        path('', views.panitia_home, name='panitia_home'),
        path('list/', views.show_homelist, name='show_homelist'),
        path('add/', views.show_addpertandingan, name='show_addpertandingan'),
        path('stadium/', views.show_liststadium, name='show_liststadium'),
        path('buat/', views.show_buatpertandingan, name='show_buatpertandingan'),
        path('pertandingan/', show_pertandingan, name='show_pertandingan'),
        path('rapat/', show_rapat, name='show_rapat'),
]