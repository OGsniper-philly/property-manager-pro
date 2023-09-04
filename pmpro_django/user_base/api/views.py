from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from user_base.models import Property, Tenant
from user_base.api.serializers import TenantSerializer, PropertySerializer

from user_auth.models import User


class CreateProperty(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create a property in the database. Restricted to landlords only.
        
        Return success status and errors (if any).

        :payload:
            address: Property address
            description: Property description
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
        
        try:
            property = Property.objects.get(address=payload["address"])
            response['success'] = False
            response['errors'].append('A property with this address already exists. Please choose another.')
        except Property.DoesNotExist:
            pass

        if response['success']:
            property = Property.objects.create(
                address=payload['address'],
                landlord=user.landlord,
                description=payload['description'],
            )
        
        return Response(response)
    
class DeleteProperty(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Delete a property in the database. Restricted to property's landlord.
        
        Return success status and errors (if any).

        :payload:
            address: Property address
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

        property = Property.objects.get(address=payload['address'])
        if property.landlord != user.landlord:
            response['success'] = False
            response['errors'].append('Permission denied.')
            return Response(response)

        if response['success']:        
            property.delete()

        return Response(response)
    
   
class RemoveTenant(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Remove a tenant from a property. Restricted to tenant's landlord.
        
        Return success status and errors (if any).

        :payload:
            username: Tenant username
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
        
        tenant_user = User.objects.get(username=payload['username'])
        tenant = tenant_user.tenant
        if tenant.property.landlord != user.landlord:
            response['success'] = False
            response['errors'].append('Permission denied.')
            return Response(response)

        if response['success']:
            tenant.property = None
            tenant.save()

        return Response(response)

class GetProperties(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return a list of properties and its tenants associated with a user.
        None if landlord or tenant have no properties.
        """
        user = request.user

        data = list()

        if user.is_landlord:
            landlord = user.landlord
            properties = landlord.property_set.all()

            if not properties:
                return Response(None)

            for property in properties:
                entry = dict()

                property_serializer = PropertySerializer(property)
                entry['property'] = property_serializer.data

                tenants = property.tenant_set.all()
                entry['tenants'] = []
                for tenant in tenants:
                    tenant_serializer = TenantSerializer(tenant)
                    entry['tenants'].append(tenant_serializer.data)

                data.append(entry)
        else:
            tenant = user.tenant
            
            if not tenant.property:
                return Response(None)
            
            entry = dict()

            property = tenant.property
            property_serializer = PropertySerializer(property)
            entry['property'] = property_serializer.data

            tenants = property.tenant_set.all()
            entry['tenants'] = []
            for tenant in tenants:
                tenant_serializer = TenantSerializer(tenant)
                entry['tenants'].append(tenant_serializer.data)

            data.append(entry)
        
        return Response(data)
    
class GetTenants(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Return a list of tenants based on a query.
        
        :payload:
            query: String to query database
        """
        payload = request.data
        query = payload['query']

        if query == '':
            tenants = Tenant.objects.all()

            if not tenants:
                return Response(None)
        else:
            tenants = Tenant.objects.none()
            query = query.split()
            for q in query:
                queryset = Tenant.objects.filter(
                    Q(user__username__icontains=q) |
                    Q(user__first_name__icontains=q) |
                    Q(user__last_name__icontains=q)
                )
                tenants |= queryset

        serializer = TenantSerializer(tenants, many=True)
        return Response(serializer.data)


class LeaveProperty(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Remove a tenant from its property. Restricted to tenants only.
        
        Return success status and errors (if any).

        :payload:
        """
        user = request.user

        response = dict()
        response['success'] = True
        response['errors'] = []
        if user.is_landlord:
            response['success'] = False
            response['errors'].append('Permission denied.')
            return Response(response)

        tenant = user.tenant
        tenant.property = None
        tenant.save()

        return Response(response)

