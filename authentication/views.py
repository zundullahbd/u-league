from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from utils.query import *
from django.contrib import messages


def homepage(request):
    return render(request, "welcome_page.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if verify(request):
            username = str(request.session["username"])
            password = str(request.session["password"])
        else:
            username = str(request.POST["username"])
            password = str(request.POST["password"])

        if not username or not password :
            messages.error(request, "Username atau password salah")
            print('ERROR salah uname/pw')
            return render(request, "login.html")

        print(username, password)

        role = get_role(username)
        print(role)

        if role == "" or role == None:
            if username and password:
                messages.error(request, "Username atau password salah")
                print('ERROR salah login')
                return render(request, "login.html")
            print("gatau dah")
            return render(request, "login.html")
        
        else:
            request.session["username"] = username
            request.session["password"] = password
            request.session["role"] = role
            request.session.set_expiry(0)
            request.session.modified = True
  
            print('masuk')
            if role == "Manajer":
                return redirect("/manager/")
            
            elif role == "Panitia":
                return redirect("/panitia/")
            
            elif role == "Penonton":
                return redirect("/penonton/")

        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     return redirect('home')  # Ganti 'home' dengan URL tujuan setelah berhasil login
        # else:
        #     error_message = "Username atau password salah."
        #     return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register_manager(request):
    return render(request, 'managerlogin.html')

def register_panitia(request):
    return render(request, 'panitialogin.html')

def register_penonton(request):
    return render(request, 'penontonlogin.html')

def logout(request):
    request.session.flush()
    request.session.clear_expired()
    print("BERHASIL LOGOUT HARUSNYA")
    return render(request, "welcome_page.html")

def register_view(request):
    return render(request, "register.html")

@csrf_exempt
def register_form(request):
    return render(request, 'register.html')

def verify(request):
    try:
        request.session["username"]
        return True
    except:
        return False
    
def get_role(username):
    res = query(f"SELECT * FROM MANAJER WHERE username='{username}'")
    if len(res) > 0:
        return "Manajer"
    
    res = query(f"SELECT * FROM PANITIA WHERE username='{username}'")
    if len(res) > 0:
        return "Panitia"
    
    res = query(f"SELECT * FROM PENONTON WHERE username='{username}'")
    if len(res) > 0:
        return "Penonton"