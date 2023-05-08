from django.urls import path
from manage_pertandingan.views import show_incomplete, show_tablelist, show_listperistiwa, show_finished

app_name = 'manage_pertandingan'

urlpatterns = [
    path('incomplete/', show_incomplete, name='show_incomplete'),
    path('tablelist/', show_tablelist, name='show_tablelist'),
    path('listperistiwa/', show_listperistiwa, name='show_listperistiwa'),
    path('finished/', show_finished, name='show_finished'),
]