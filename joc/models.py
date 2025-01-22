from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

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

    def __str__(self):
        return self.username
