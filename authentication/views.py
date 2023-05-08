from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout


def homepage(request):
    return render(request, "welcome_page.html")

def login(request):
    return render(request, "login.html")

def register_manager(request):
    return render(request, 'managerlogin.html')

def register_panitia(request):
    return render(request, 'panitialogin.html')

def register_penonton(request):
    return render(request, 'penontonlogin.html')

def logout(request):
    return render(request, "welcome_page.html")

def register_view(request):
    return render(request, "register.html")

@csrf_exempt
def register_form(request):
    return render(request, 'register.html')
    
