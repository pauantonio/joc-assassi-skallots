from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import csv
from datetime import datetime
import random

class Player(AbstractUser):
    PLAYER_STATUS_CHOICES = [
        ('pending_registration', _('Pendent de registre')),
        ('waiting_for_circle', _('Esperant a formar part del cercle')),
        ('not_playing', _('No jugant')),
        ('alive', _('Viu')),
        ('pending_death_confirmation', _('Pendent de confirmació de mort')),
        ('dead', _('Mort')),
        ('last_player_standing', _('Últim jugador viu')),
        ('banned', _('Expulsat'))
    ]

    first_name = None
    last_name = None
    password = None
    is_staff = None
    is_active = None
    email = None
    groups = None
    user_permissions = None
    date_joined = None
    is_superuser = None
    username = None

    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=200, null=False, default="")
    birth_date = models.DateField()
    status = models.CharField(max_length=30, choices=PLAYER_STATUS_CHOICES, default='pending_registration')

    def save(self, *args, **kwargs):
        if len(self.code) != 5:
            raise ValidationError('Code must be exactly 5 characters long')
        
        if self.pk:
            old_instance = Player.objects.get(pk=self.pk)
                
            if old_instance.status != self.status and self.status == 'banned':
                AssassinationCircle.ban_player(self)

        super().save(*args, **kwargs)

    @classmethod
    def import_from_csv(cls, csv_file):
        # Import players from a CSV file
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                player = cls(
                    name=row['Nom i Cognoms'],
                    birth_date=datetime.strptime(row['Data de Naixement'], '%d/%m/%Y').date(),
                    code=row['Codi'],
                )
                player.save()
            except ValidationError as e:
                print(f"Error saving player {row['Nom i Cognoms']}: {e}")
            except ValueError as e:
                print(f"Error parsing date for player {row['Nom i Cognoms']}: {e}")

    def __str__(self):
        return f"{self.name}"

# Game settings model
class GameConfig(models.Model):
    GAME_STATUS_CHOICES = [
        ('disabled_until_time', 'Esperant a començar'),
        ('playing', 'Jugant'),
        ('paused', 'Pausat'),
        ('finished', 'Finalitzat')
    ]
    
    disable_until = models.DateTimeField(default=datetime(2025, 7, 14, 18, 0, 0))
    game_status = models.CharField(max_length=20, choices=GAME_STATUS_CHOICES, default='disabled_until_time')
    
    def save(self, *args, **kwargs):
        if not self.pk and GameConfig.objects.exists():
            raise ValidationError('There can be only one GameConfig instance')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "Game Settings"

class AssassinationCircle(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='assassin')
    target = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='targeted_by')

    def __str__(self):
        return f"{self.player} -> {self.target}"

    @classmethod
    def create_circle(cls):
        players = list(Player.objects.filter(status='waiting_for_circle'))
        if len(players) < 2:
            raise ValidationError('At least two players are required to create an assassination circle.')
        
        random.shuffle(players)
        for i in range(len(players)):
            cls.objects.create(player=players[i], target=players[(i + 1) % len(players)])
            players[i].status = 'alive'
            players[i].save()

        players_not_enrolled = Player.objects.filter(status='pending_registration')

        for player in players_not_enrolled:
            player.status = 'not_playing'
            player.save()

    @classmethod
    def request_kill(cls, killer):
        if killer.status != 'alive':
            return

        killer_circle = cls.objects.get(player=killer)
        victim = killer_circle.target
        if victim.status == 'alive':
            victim.status = 'pending_death_confirmation'
            victim.save()
        else:
            raise ValidationError('Your victim is already dead or pending death confirmation.')
        
    @classmethod
    def revert_kill(cls, killer):
        if killer.status != 'alive':
            return

        killer_circle = cls.objects.get(player=killer)
        victim = killer_circle.target
        if victim.status == 'pending_death_confirmation':
            victim.status = 'alive'
            victim.save()
        else:
            raise ValidationError('Your victim is not pending death confirmation.')

    @classmethod
    def confirm_death(cls, victim):
        if victim.status != 'pending_death_confirmation':
            return

        victim_circle = cls.objects.get(player=victim)
        killer_circle = cls.objects.get(target=victim)

        killer = killer_circle.player
        
        # Check if the victim is the last standing player
        if killer == victim_circle.target:
            killer.status = 'last_player_standing'
            killer.save()
            killer_circle.delete()
            victim_circle.delete()

        else:
            killer_circle.target = victim_circle.target
            victim_circle.delete()
            killer_circle.save()
        
        victim.status = 'dead'
        victim.save()

        # Assign points based on the specified criteria
        if killer.status == 'last_player_standing':
            points = 1000
        else:
            points = 200

        Assassination.objects.create(killer=killer, victim=victim, points=points)

    @classmethod
    def discard_death(cls, victim):
        if victim.status != 'pending_death_confirmation':
            return

        victim.status = 'alive'
        victim.save()

    @classmethod
    def ban_player(cls, player):
        player_circle = cls.objects.get(player=player)
        victim = player_circle.target
        player_circle.delete()

        player_target_circle = cls.objects.get(target=player)

        if player_target_circle.player == victim:
            victim.status = 'last_player_standing'
            victim.save()

        else:
            if victim.status == 'pending_death_confirmation':
                victim.status = 'alive'
                victim.save()

            player_target_circle.target = victim
            player_target_circle.save()

        Assassination.objects.create(killer=player, victim=player, points=0)

class Assassination(models.Model):
    ASSASSINATION_POINTS_CHOICES = [
        (0, '0 - Expulsat'),
        (200, '200 - Cas general'),
        (1000, '1000 - Últim jugador viu'),
    ]

    killer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='kills')
    victim = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='deaths')
    timestamp = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=200, choices=ASSASSINATION_POINTS_CHOICES)

    def __str__(self):
        return f"{self.killer} killed {self.victim} on {self.timestamp}"
