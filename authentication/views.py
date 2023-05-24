from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from utils.query import *


def homepage(request):
    return render(request, "welcome_page.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Ganti 'home' dengan URL tujuan setelah berhasil login
        else:
            error_message = "Username atau password salah."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

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
    
