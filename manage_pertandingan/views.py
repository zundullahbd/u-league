from django.shortcuts import render

# Create your views here.
def show_incomplete(request):
    return render(request, "incomplete.html")

def show_listperistiwa(request):
    return render(request, "listperistiwa.html")

def show_tablelist(request):
    return render(request, "tablelist.html")

def show_finished(request):
    return render(request, "finished.html")