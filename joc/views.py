from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import PlayerProfileForm, PlayerLoginForm
from .models import GameSettings
from django.utils.timezone import localtime, now
from functools import wraps

def game_not_paused(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        settings = GameSettings.objects.first()
        if settings is not None and (settings.game_status == 'paused' or (settings.game_status == 'disabled_until_time' and now() < settings.disable_until)):
            return JsonResponse({'error': 'Game is paused or disabled until a certain time.'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def index(request):
    if request.user.is_authenticated:
        return menu_view(request)
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
            if request.GET.get('next'):
                return redirect(request.GET['next'])
            return redirect('index')
        else:
            form.add_error(None, 'Codi o data de naixement incorrectes. Comprova que les dades són correctes i torna a intentar-ho.')
    return render(request, 'login.html', {'form': form})

@login_required
def menu_view(request):
    return render(request, 'menu.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        return handle_profile_post(request)
    else:
        form = PlayerProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def handle_profile_post(request):
    form = PlayerProfileForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'profile.html', {'form': form})

@login_required
@game_not_paused
def victim_view(request):
    return render(request, 'profile.html')

def logout_view(request):
    logout(request)
    response = redirect('index')
    response.delete_cookie('sessionid')
    return response

def game_settings(request):
    settings = GameSettings.objects.first()
    if settings is None:
        return JsonResponse({
            'disable_until': None,
            'game_status': 'playing',
        })
    return JsonResponse({
        'disable_until': localtime(settings.disable_until).isoformat(),
        'game_status': settings.game_status,
    })
