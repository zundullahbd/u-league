from django.shortcuts import render

# Create your views here.
def penonton_home(request):
    return render(request, 'penonton_home.html')