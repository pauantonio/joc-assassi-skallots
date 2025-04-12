from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from joc.models import Player

class AdminPanelLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin'):
            if isinstance(request.user, Player):
                logout(request)
                return redirect(reverse('admin:login'))

        elif not request.path.startswith('/admin'):
            if request.user.is_staff:
                logout(request)
                return redirect('login')

        return self.get_response(request)
