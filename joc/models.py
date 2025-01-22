from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import csv
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils.timezone import now

class Player(AbstractUser):
    code = models.CharField(max_length=50, unique=True)  # Codi únic
    birth_date = models.DateField()  # Data de naixement
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Foto de perfil
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='player_set',  # Add related_name to avoid clash
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='player',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='player_set',  # Add related_name to avoid clash
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_query_name='player',
    )

    def save(self, *args, **kwargs):
        if self.pk and self.profile_picture:
            # Get the original file extension
            ext = self.profile_picture.name.split('.')[-1]
            # Set the new filename using user ID and timestamp
            self.profile_picture.name = f"{self.pk}_{now().strftime('%Y%m%d%H%M%S')}.{ext}"
        super().save(*args, **kwargs)

    @classmethod
    def import_from_csv(cls, csv_file):
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                player = cls(
                    username=f"{row['Name']}_{row['Surname']}_{row['Code']}",
                    first_name=row['Name'],
                    last_name=row['Surname'],
                    birth_date=datetime.strptime(row['Birthday'], '%d/%m/%Y').date(),
                    code=row['Code']
                )
                player.save()
            except ValidationError as e:
                print(f"Error saving player {row['Name']}: {e}")
            except ValueError as e:
                print(f"Error parsing date for player {row['Name']}: {e}")

    def __str__(self):
        return self.username
