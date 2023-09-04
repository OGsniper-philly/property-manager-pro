from django.urls import path

from .views import CreateProperty, DeleteProperty, GetProperties, GetTenants, LeaveProperty, RemoveTenant


"""
API descriptions:

:route create-property/: (post) expects property data, attempts to create property in database
:route delete-property/: (post) expects property address, deletes if landlord has permissions
:route remove-tenant/: (post) expects tenant username, removes from property if landlord has permissions
:route leave-property/: (post) removes tenant from its property
:route get-properties/: (get) gets all properties and their tenants associated a user
:route get-tenants/: (post) expects query, gets all tenants associated with query
"""
urlpatterns = [
    # Landlord APIs
    path('create-property/', CreateProperty.as_view(), name="create_property"),
    path('delete-property/', DeleteProperty.as_view(), name='delete_property'),
    path('remove-tenant/', RemoveTenant.as_view(), name='remove_tenant'),
    # Tenant APIs
    path('leave-property/', LeaveProperty.as_view(), name='leave_property'),
    # Both
    path('get-properties/', GetProperties.as_view(), name='get_properties'),
    path('get-tenants/', GetTenants.as_view(), name='get_tenants'),  
]