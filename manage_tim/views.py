from django.shortcuts import render

# Create your views here.
def show_timregist(request):
    return render(request, "teamregist.html")