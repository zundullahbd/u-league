from django.urls import path
from manage_tim.views import show_timregist

app_name = 'manage_tim'

urlpatterns = [
    path('registrasi/', show_timregist, name='show_timregist'),
]