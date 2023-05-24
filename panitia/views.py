from django.shortcuts import render

# Create your views here.
def panitia_home(request):
    return render(request, 'panitia_home.html')

def show_homelist(request):
    return render(request, "homelist.html")

def show_addpertandingan(request):
    return render(request, "addpertandingan.html")

def show_liststadium(request):
    return render(request, "liststadium.html")

def show_buatpertandingan(request):
    return render(request, "buatpertandingan.html")

# untuk rapat
def show_pertandingan(request):
    return render(request, "pilihpertandingan.html")

# untuk rapat
def show_rapat(request):
    return render(request, "rapat.html")