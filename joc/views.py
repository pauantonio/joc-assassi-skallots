from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import PlayerLoginForm
from .models import GameConfig, AssassinationCircle, Assassination, Player
from django.utils.timezone import localtime
from functools import wraps
from django.views.decorators.http import require_POST
from django.db.models import Count, Sum

def game_not_paused(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        settings = GameConfig.objects.first()
        if settings is not None and settings.game_status == 'paused':
            if view_func.__name__ == 'request_kill':
                return redirect('victim')
            return render(request, '404.html')
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
def rules_view(request):
    return render(request, 'rules.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@require_POST
@login_required
def register_to_game(request):
    user = request.user
    if user.status == 'pending_registration':
        user.status = 'waiting_for_circle'
        user.save()
    return redirect('profile')

@login_required
def victim_view(request):
    player = request.user
    victim = None
    killer = None
    try:
        if player.status == 'alive':
            victim = AssassinationCircle.objects.get(player=player).target
        elif player.status == 'pending_death_confirmation':
            killer = AssassinationCircle.objects.get(target=player).player
        elif player.status == 'dead':
            killer = Assassination.objects.get(victim=player).killer
        victims_history = Assassination.objects.filter(killer=player, points__gt=0).order_by('-timestamp')
    except AssassinationCircle.DoesNotExist:
        pass
    return render(request, 'victim.html', {'status': player.status, 'victim': victim, 'killer': killer, 'victims_history': victims_history})

@login_required
@require_POST
@game_not_paused
def request_kill(request):
    player = request.user
    try:
        AssassinationCircle.request_kill(player)
        return redirect('victim')
    except AssassinationCircle.DoesNotExist:
        return redirect('victim')

@login_required
@require_POST
def revert_kill(request):
    player = request.user
    try:
        AssassinationCircle.revert_kill(player)
        return redirect('victim')
    except AssassinationCircle.DoesNotExist:
        return redirect('victim')

@login_required
@require_POST
def confirm_death(request):
    player = request.user
    try:
        AssassinationCircle.confirm_death(player)
        return redirect('victim')
    except AssassinationCircle.DoesNotExist:
        return redirect('victim')

@login_required
@require_POST
def discard_death(request):
    player = request.user
    try:
        AssassinationCircle.discard_death(player)
        return redirect('victim')
    except AssassinationCircle.DoesNotExist:
        return redirect('victim')

@login_required
def ranking_view(request):
    assassinations = Assassination.objects.filter(points__gt=0).values('killer').annotate(
        victims=Count('victim'),
        total_points=Sum('points'),
    ).order_by('-total_points')

    player_details = []
    for entry in assassinations:
        player = Player.objects.get(id=entry['killer'])
        player_details.append({
            'player': player,
            'name': player.name,
            'total_victims': entry['victims'],
            'total_points': entry['total_points'],
            'is_self': player == request.user,
        })

    return render(request, 'ranking.html', {'player_details': player_details})

@login_required
def cemetery_view(request):
    assassinations = Assassination.objects.values('victim', 'timestamp').order_by('-timestamp')

    victim_details = []
    for entry in assassinations:
        victim = Player.objects.get(id=entry['victim'])
        victim_details.append({
            'victim': victim,
            'name': victim.name,
            'timestamp': localtime(entry['timestamp']).strftime('%d/%m/%Y %H:%M h'),
        })

    total_players = Player.objects.filter(status__in=['dead', 'banned', 'pending_death_confirmation', 'alive', 'last_player_standing']).count()
    total_dead = Player.objects.filter(status__in=['dead', 'banned']).count()

    stats = {
        'total_players': total_players,
        'total_dead': total_dead
    }

    return render(request, 'cemetery.html', {'victim_details': victim_details, 'stats': stats})

def logout_view(request):
    logout(request)
    response = redirect('index')
    response.delete_cookie('sessionid')
    return response

def game_settings(request):
    settings = GameConfig.objects.first()
    if settings is None:
        return JsonResponse({
            'start_time': None,
            'game_status': 'playing',
        })
    return JsonResponse({
        'start_time': localtime(settings.disable_until).isoformat(),
        'game_status': settings.game_status,
    })

def player_view(request, id):
    player = Player.objects.get(id=id)
    return render(request, 'player.html', {'player': player})

@login_required
def player_victim_status(request):
    player = request.user
    player_status = player.status
    try:
        victim = AssassinationCircle.objects.get(player=player).target
        return JsonResponse({'player_status': player_status, 'victim_status': victim.status})
    except AssassinationCircle.DoesNotExist:
        return JsonResponse({'player_status': player_status, 'victim_status': 'dead'})
