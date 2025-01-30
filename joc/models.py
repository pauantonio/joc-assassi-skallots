from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.timezone import now
import csv
from datetime import datetime

# Custom Player model extending AbstractUser
class Player(AbstractUser):
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

    def save(self, *args, **kwargs):
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
                    first_name=row['Name'],
                    last_name=row['Surname'],
                    birth_date=datetime.strptime(row['Birthday'], '%d/%m/%Y').date(),
                    code=row['Code'],
                    esplai=row['Esplai'],
                    territori_zona=row['Territori'],
                )
                player.save()
            except ValidationError as e:
                print(f"Error saving player {row['Name']}: {e}")
            except ValueError as e:
                print(f"Error parsing date for player {row['Name']}: {e}")

    def __str__(self):
        return self.code

# Game settings model
class GameSettings(models.Model):
    GAME_STATUS_CHOICES = [
        ('playing', 'Playing'),
        ('disabled_until_time', 'Disabled Until Time'),
        ('paused', 'Paused'),
    ]
    
    disable_until = models.DateTimeField(default=now().replace(year=2025, month=3, day=22, hour=12, minute=0, second=0))
    game_status = models.CharField(max_length=20, choices=GAME_STATUS_CHOICES, default='playing')
    
    def save(self, *args, **kwargs):
        if not self.pk and GameSettings.objects.exists():
            raise ValidationError('There can be only one GameSettings instance')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "Game Settings"

from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Ensure a GameSettings instance is created after migrations
@receiver(post_migrate)
def create_game_settings(sender, **kwargs):
    if not GameSettings.objects.exists():
        GameSettings.objects.create()
