from django.contrib import admin

from .models import Tenant, Landlord


admin.site.register(Landlord)
admin.site.register(Tenant)
