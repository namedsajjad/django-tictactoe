from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from .models import Player, Game

def index(request):
    return render(request, 'game/index.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not username or not email or not password1 or not password2:
            return render(request, 'auth/register.html', {'error': 'All fields are required.'})
        if password1 != password2:
            return render(request, 'auth/register.html', {'error': 'Passwords do not match.'})
        try:
            Player.objects.get(username=username)
            return render(request, 'auth/register.html', {'error': 'Username already exists.'})
        except Player.DoesNotExist:
            pass
        user = Player.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        login(request, user)
        return redirect('index')
    return render(request, 'auth/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'auth/login.html')
    return render(request, 'auth/login.html')

@login_required
def logout_view(request):
    print("Logging out user:", request.user.username)
    logout(request)
    return redirect('index')