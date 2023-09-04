from django.db import models

from user_auth.models import User


class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name} @{self.user.username}'



class Property(models.Model):
    address = models.CharField(max_length=200)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return f"{self.address} - {self.landlord.user.first_name} {self.landlord.user.last_name} @{self.landlord.user.username}"


class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name} @{self.user.username}'