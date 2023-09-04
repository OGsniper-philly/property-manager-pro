from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from user_auth.models import User
from user_base.models import Landlord, Tenant

 
class CreateUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Create a user in the database. 
        
        Return success status and errors (if any).

        :payload:
            first: First name
            last: Last name
            username: Username
            email: Email
            password: Password
            is_landlord: True if landlord, False otherwise
        """
        payload = request.data

        response = dict()
        response['success'] = True
        response['errors'] = []

        try:
            user = User.objects.get(email=payload['email'])
            response['success'] = False
            response['errors'].append('This email is already registered with a user. Please login.')
        except User.DoesNotExist:
            pass

        try:
            user = User.objects.get(username=payload['username'])
            response['success'] = False
            response['errors'].append('Username already exists. Please choose another.')
        except User.DoesNotExist:
            pass
        
        if response['success']:
            user = User.objects.create_user(
                first_name = payload['first'],
                last_name = payload['last'],
                username = payload['username'],
                email = payload['email'],
                password = payload['password'],
                is_landlord = payload['is_landlord']
            )
            if payload['is_landlord']:
                Landlord.objects.create(user=user)
            else:
                Tenant.objects.create(user=user)
        
        return Response(response)

class UpdateUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Update a user in the database. 
        
        Return success status and errors (if any).

        :payload:
            first: First name
            last: Last name
            username: Username
            email: Email
        """
        payload = request.data
        user = request.user

        response = dict()
        response['success'] = True
        response['errors'] = []

        if user.email != payload['email']:
            try:
                other_user = User.objects.get(email=payload['email'])
                response['success'] = False
                response['errors'].append('This email is already registered with a user. Please choose another.')
            except User.DoesNotExist:
                pass


        if user.username != payload['username']:
            try:
                other_user = User.objects.get(username=payload['username'])
                response['success'] = False
                response['errors'].append('Username already exists. Please choose another.')
            except User.DoesNotExist:
                pass
        
        if response['success']:
            user.first_name = payload['first']
            user.last_name = payload['last']
            user.email = payload['email']
            user.username = payload['username']
            user.save()

        return Response(response)
    
class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Delete the user in the database. 
        
        Return success status and errors (if any).

        :payload: None
        """
        user = request.user

        response = dict()
        response['success'] = True
        response['errors'] = []
        
        user.delete()

        return Response(response)

