from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from user_auth.models import User
from user_base.models import Property
from user_connect.models import Invitation

from .serializers import InvitationSerializer


class CreateInvitation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create an invitation to a tenant so they can join a property. Restricted to property's landlord.
        
        Return success status and errors (if any).

        :payload:
            tenant_username: Tenant's username to invite
            property_address: Address of landlord's property
        """
        payload = request.data
        user = request.user

        response = dict()
        response['success'] = True
        response['errors'] = []
        if not user.is_landlord:
            response['success'] = False
            response['errors'].append('Permission denied.')
            return Response(response)
        
        property = Property.objects.get(address=payload['property_address'])
        if property.landlord != user.landlord:
            response['success'] = False
            response['errors'].append('Permission denied.')
            return Response(response)
        
        tenant_user = User.objects.get(username=payload['tenant_username'])
        tenant = tenant_user.tenant
        try:
            invitation = Invitation.objects.get(tenant=tenant, property=property)
            response['success'] = False
            response['errors'].append('This invitation has already been sent.')
        except Invitation.DoesNotExist:
            pass

        if tenant.property != None:
            if tenant.property == property:
                response['success'] = False
                response['errors'].append('This tenant is already apart of your property.')
        
        if response['success']:
            invitation = Invitation.objects.create(
                tenant=tenant,
                property=property
            )

        return Response(response)
 
class DeleteInvitation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Delete an invitation from a landlord to a tenant to join their property.
        
        Return success status and errors (if any).

        :payload:
            tenant_username: Username of tenant associated with invite
            property_address: Address of landlord's property
        """
        payload = request.data
        user = request.user

        response = dict()
        response['success'] = True
        response['errors'] = []

        property = Property.objects.get(address=payload['property_address'])
        tenant_user = User.objects.get(username=payload['tenant_username'])
        tenant = tenant_user.tenant

        if user.is_landlord:
            if property.landlord != user.landlord:
                response['success'] = False
                response['errors'].append('Permission denied.')
                return Response(response)
        else:
            if tenant != user.tenant:
                response['success'] = False
                response['errors'].append('Permission denied.')
                return Response(response)

        invitation = Invitation.objects.get(property=property, tenant=tenant)
        invitation.delete()

        return Response(response)

class GetInvitations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return a list of invitations associated with a user.
        None if landlord or tenant have no invitations.
        """
        user = request.user

        if user.is_landlord:
            landlord = user.landlord
            properties = landlord.property_set.all()

            invitations = Invitation.objects.none()

            for property in properties:
                query_set = property.invitation_set.all()
                invitations |= query_set
        else:
            tenant = user.tenant
            invitations = tenant.invitation_set.all()
        
        if not invitations:
            return Response(None)
        
        serializer = InvitationSerializer(invitations, many=True)
        return Response(serializer.data)
    
class AcceptInvitation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Accept an invitation from a landlord and join their property. Restricted to tenant's only.
        
        Return success status and errors (if any).

        :payload:
            address: The address associated with invitation
        """
        payload = request.data
        user = request.user
        
        response = dict()
        response['success'] = True
        response['errors'] = []
        if user.is_landlord:
            response['success'] = False
            response['errors'].append('Permission denied.')
            return Response(response)

        tenant = user.tenant
        if tenant.property != None:
            response['success'] = False
            response['errors'].append('You are already associated with a property. Please leave before you join another.')
            return Response(response)

        property = Property.objects.get(address=payload['address'])
        try:
            invitation = Invitation.objects.get(tenant=tenant, property=property)
            invitation.delete()
            tenant.property = property
            tenant.save()
        except Invitation.DoesNotExist:
            response['success'] = False
            response['errors'].append('Permission denied.')

        return Response(response)


