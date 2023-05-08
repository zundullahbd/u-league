from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime;


def homepage(request):
    return render(request, "welcome_page.html")

def login(request):
    return render(request, "login.html")

def register_manager(request):
    return render(request, 'managerlogin.html')

def register_panitia(request):
    return render(request, 'panitialogin.html')

def register_pelanggan(request):
    return render(request, 'pelangganlogin.html')

def logout(request):

    return render(request, "welcome_page.html")


    
