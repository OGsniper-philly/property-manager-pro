from django.db import models

from user_auth.models import User
from user_base.models import Property, Tenant


class Invitation(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.property.address} to {self.tenant.user.first_name}@{self.tenant.user.username}"

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body[0:50]
    