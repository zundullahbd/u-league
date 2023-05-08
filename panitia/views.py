from django.shortcuts import render

# Create your views here.
def panitia_home(request):
    return render(request, 'panitia_home.html')