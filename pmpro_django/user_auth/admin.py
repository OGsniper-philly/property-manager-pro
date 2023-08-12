from django.contrib import admin

from .models import Profile, Landlord, Tenant

admin.site.register(Profile)
admin.site.register(Landlord)
admin.site.register(Tenant)