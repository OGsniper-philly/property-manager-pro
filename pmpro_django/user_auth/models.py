from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.username}'

class Landlord(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f'{self.profile.user.username}'

class Tenant(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    landlord = models.ForeignKey(Landlord, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'{self.profile.user.username}'