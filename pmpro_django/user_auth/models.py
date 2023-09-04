from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model.

    All accounts will be linked to this model.
    """
    is_landlord = models.BooleanField(null=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} @{self.username}'