"""
URL configuration for joc_assassi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from joc import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('rules/', views.rules_view, name='rules'),
    path('profile/', views.profile_view, name='profile'),
    path('register-to-game/', views.register_to_game, name='register_to_game'),
    path('victim/', views.victim_view, name='victim'),
    path('ranking/', views.ranking_view, name='ranking'),
    path('cemetery/', views.cemetery_view, name='cemetery'),
    path('logout/', views.logout_view, name='logout'),
    path('api/game-settings/', views.game_settings, name='game-settings'),
    path('request_kill/', views.request_kill, name='request_kill'),
    path('revert_kill/', views.revert_kill, name='revert_kill'),
    path('confirm_death/', views.confirm_death, name='confirm_death'),
    path('discard_death/', views.discard_death, name='discard_death'),
    path('player/<int:id>/', views.player_view, name='player'),
    path('api/player-victim-status/', views.player_victim_status, name='player-victim-status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
