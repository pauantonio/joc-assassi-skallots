from django.contrib.auth.backends import BaseBackend
from .models import Player

class CodeBirthDateBackend(BaseBackend):
    def authenticate(self, request, code=None, birth_date=None):
        try:
            player = Player.objects.get(code=code, birth_date=birth_date)
            return player
        except Player.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Player.objects.get(pk=user_id)
        except Player.DoesNotExist:
            return None
