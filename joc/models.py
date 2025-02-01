from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.timezone import now
import csv
from datetime import datetime
import random

# Custom Player model extending AbstractUser
class Player(AbstractUser):
    PLAYER_STATUS_CHOICES = [
        ('alive', _('Viu')),
        ('pending_death_confirmation', _('Pendent de confirmació de mort')),
        ('dead', _('Mort')),
    ]

    # Remove unused fields from AbstractUser
    password = None
    is_staff = None
    is_active = None
    email = None
    groups = None
    user_permissions = None
    date_joined = None
    is_superuser = None
    username = None

    # Custom fields for Player model
    code = models.CharField(max_length=5, unique=True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=150, null=False)
    birth_date = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    territori_zona = models.CharField(max_length=50, default="")
    esplai = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=30, choices=PLAYER_STATUS_CHOICES, default='alive')

    def save(self, *args, **kwargs):
        # Validate code length
        if len(self.code) != 5:
            raise ValidationError('Code must be exactly 5 characters long')
        # Rename profile picture if it has changed
        if self.pk:
            old_instance = Player.objects.get(pk=self.pk)
            if old_instance.profile_picture != self.profile_picture:
                ext = self.profile_picture.name.split('.')[-1]
                self.profile_picture.name = f"{self.code}_{now().strftime('%Y%m%d%H%M%S')}.{ext}"
        super().save(*args, **kwargs)

    @classmethod
    def import_from_csv(cls, csv_file):
        # Import players from a CSV file
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                player = cls(
                    first_name=row['Nom'],
                    last_name=row['Cognoms'],
                    birth_date=datetime.strptime(row['Data de Naixement'], '%d/%m/%Y').date(),
                    code=row['Codi'],
                    esplai=row['Centre'],
                    territori_zona=row['Territori/Zona'],
                )
                player.save()
            except ValidationError as e:
                print(f"Error saving player {row['Nom']} {row['Cognoms']}: {e}")
            except ValueError as e:
                print(f"Error parsing date for player {row['Nom']} {row['Cognoms']}: {e}")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.esplai} - {self.territori_zona})"

# Game settings model
class GameConfig(models.Model):
    GAME_STATUS_CHOICES = [
        ('playing', 'Playing'),
        ('disabled_until_time', 'Disabled Until Time'),
        ('paused', 'Paused'),
    ]
    
    disable_until = models.DateTimeField(default=now().replace(year=2025, month=3, day=22, hour=12, minute=0, second=0))
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
        players = list(Player.objects.all())
        if len(players) < 2:
            raise ValidationError('At least two players are required to create an assassination circle.')
        
        random.shuffle(players)
        for i in range(len(players)):
            cls.objects.create(player=players[i], target=players[(i + 1) % len(players)])

    @classmethod
    def update_circle(cls, killer):
        killer_circle = cls.objects.get(player=killer)
        victim = killer_circle.target
        if victim.status == 'alive':
            victim.status = 'pending_death_confirmation'
            victim.save()
            Assassination.objects.create(killer=killer, victim=victim)
        else:
            raise ValidationError('Your victim is already dead or pending death confirmation.')

    @classmethod
    def confirm_death(cls, victim):
        victim_circle = cls.objects.get(player=victim)
        killer_circle = cls.objects.get(target=victim)
        killer_circle.target = victim_circle.target
        victim_circle.delete()
        killer_circle.save()
        victim.status = 'dead'
        victim.save()

        # Assign points based on the specified criteria
        killer = killer_circle.player
        if killer.esplai == victim.esplai:
            points = 100
        elif killer.territori_zona == victim.territori_zona:
            points = 150
        else:
            points = 200

        Assassination.objects.create(killer=killer, victim=victim, points=points)

class Assassination(models.Model):
    ASSASSINATION_POINTS_CHOICES = [
        (100, '100 - Esplai'),
        (150, '150 - Territori/Zona'),
        (200, '200 - MCECC'),
    ]

    killer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='kills')
    victim = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='deaths')
    timestamp = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=200, choices=ASSASSINATION_POINTS_CHOICES)

    def __str__(self):
        return f"{self.killer} killed {self.victim} on {self.timestamp}"

from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Ensure a GameConfig instance is created after migrations
@receiver(post_migrate)
def create_game_settings(sender, **kwargs):
    if not GameConfig.objects.exists():
        GameConfig.objects.create()
