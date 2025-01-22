from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import PlayerProfileForm, PlayerLoginForm

def login_view(request):
    if request.method == 'POST':
        form = PlayerLoginForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            birth_date = form.cleaned_data['birth_date']
            player = authenticate(request, code=code, birth_date=birth_date)
            if player is not None:
                login(request, player)
                return redirect('profile')
            else:
                form.add_error(None, 'Invalid code or birth date')
    else:
        form = PlayerLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PlayerProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})
