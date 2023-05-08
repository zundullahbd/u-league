from django.urls import path
from r_listpertandingan.views import show_listpertandingan

app_name = 'r_listpertandingan'

urlpatterns = [
    path('listpertandingan/', show_listpertandingan, name='show_listpertandingan'),
]