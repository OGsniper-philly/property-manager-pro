from django.contrib import admin

from .models import Landlord, Tenant

admin.site.register(Landlord)
admin.site.register(Tenant)