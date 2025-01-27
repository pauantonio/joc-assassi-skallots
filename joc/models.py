from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import csv
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils.timezone import now
import json

with open('joc/static/json/choices.json') as data:
    choices = json.load(data)

class Player(AbstractUser):
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
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=150, null=False)
    birth_date = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    territori_zona = models.CharField(max_length=50, default="", choices=[(t['zona'], t['nom']) for t in choices['TERRITORIS']])
    esplai = models.CharField(max_length=100, default="")

    def save(self, *args, **kwargs):
        if self.pk and self.profile_picture:
            # Get the original file extension
            ext = self.profile_picture.name.split('.')[-1]
            # Set the new filename using user ID and timestamp
            self.profile_picture.name = f"{self.code}_{now().strftime('%Y%m%d%H%M%S')}.{ext}"
        super().save(*args, **kwargs)

    @classmethod
    def import_from_csv(cls, csv_file):
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
