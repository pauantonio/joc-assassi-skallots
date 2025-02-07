"""
URL configuration for joc_esparrek project.

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
    path('perfil/', views.profile_view, name='profile'),
    path('victim/', views.victim_view, name='victim'),
    path('ranking/', views.ranking_view, name='ranking'),
    path('cemetery/', views.cemetery_view, name='cemetery'),
    path('logout/', views.logout_view, name='logout'),
    path('api/game-settings/', views.game_settings, name='game-settings'),
    path('request_kill/', views.request_kill, name='request_kill'),
    path('confirm_death/', views.confirm_death, name='confirm_death'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
