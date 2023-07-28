from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Landlord(models.Model):
    user_profile = models.OneToOneField

class Tenant(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE)
    landlord = models.ForeignKey(Landlord, on_delete=models.SET_NULL, null=True)