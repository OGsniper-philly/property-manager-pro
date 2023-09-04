from django.contrib import admin

from .models import Property, Message, Invitation

admin.site.register(Property)
admin.site.register(Message)
admin.site.register(Invitation)