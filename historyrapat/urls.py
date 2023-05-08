from django.urls import path
from historyrapat.views import show_historyrapat

app_name = 'historyrapat'

urlpatterns =[
    path('historyrapat/', show_historyrapat, name='show_historyrapat')
]