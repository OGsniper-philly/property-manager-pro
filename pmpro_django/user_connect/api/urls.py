from django.urls import path

from .views import CreateInvitation, GetInvitations
from .views import AcceptInvitation, DeleteInvitation


"""
API descriptions:

:route create-invitation/: (post) expects tenant username and property address, creates invite if landlord has permissions
:route delete-invitation/: (post) expects tenant username and property address, deletes invite if user has permissions
:route get-invitations/: (get) gets all invitations associated with a user
:route accept-invitation/: (post) expects property address, adds tenant to property if invited
"""
urlpatterns = [
    # Landlord APIs
    path('create-invitation/', CreateInvitation.as_view(), name='create_invitation'),
    # Tenant APIs
    path('accept-invitation/', AcceptInvitation.as_view(), name='accept_invitation'),
    # Both
    path('get-invitations/', GetInvitations.as_view(), name='get_invitations'),
    path('delete-invitation/', DeleteInvitation.as_view(), name='delete_invitation'),
]