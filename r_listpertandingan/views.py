from django.shortcuts import render

# Create your views here.
def show_listpertandingan(request):
    return render(request, "listpertandingan.html")
