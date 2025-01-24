from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PlayerProfileForm, PlayerLoginForm

def index(request):
    if request.user.is_authenticated:
        return profile_view(request)
    else:
        return login_view(request)

def login_view(request):
    if request.method == 'POST':
        return handle_login_post(request)
    else:
        form = PlayerLoginForm()
    return render(request, 'login.html', {'form': form})

def handle_login_post(request):
    form = PlayerLoginForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        birth_date = form.cleaned_data['birth_date']
        player = authenticate(request, code=code, birth_date=birth_date)
        if player is not None:
            login(request, player)
            return redirect('index')
        else:
            form.add_error(None, 'Invalid code or birth date')
    return render(request, 'login.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        if 'remove_picture' in request.POST:
            request.user.profile_picture.delete()
            request.user.save()
            return redirect('index')
        return handle_profile_post(request)
    else:
        form = PlayerProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def handle_profile_post(request):
    form = PlayerProfileForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'profile.html', {'form': form})

def logout_view(request):
    logout(request)
    response = redirect('index')
    response.delete_cookie('sessionid')
    return response
