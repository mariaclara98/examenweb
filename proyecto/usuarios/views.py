from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login

# Create your views here.
def home(request):
    data = {}
    return render(request, 'examen/inicio.html', data)



def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)            
        return redirect('examen')  # Redirige a la página de inicio después de crear el usuario

    return redirect('home')

def login_usuario(request):
    if request.method == 'POST':
        email = request.POST['emailLogin']
        password = request.POST['passwordLogin']
        
        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            authenticate(request, user)
            return redirect('examen')  # Redirige a la página de inicio después de iniciar sesión
        else:
            return HttpResponse("Credenciales inválidas.")
    
    return redirect('home')