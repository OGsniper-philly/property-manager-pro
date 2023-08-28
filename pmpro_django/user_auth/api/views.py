from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User

from user_auth.models import Landlord, Tenant
from .serializers import MyTokenObtainPairSerializer


class GetRoutes(APIView):
    def get(self, request):
        routes = {
            'api/v1/auth/routes/': 'Returns all api routes for authentication and authorization.',
            'api/v1/auth/token/': 'Returns login access and refresh JWT tokens for a user.',
            'api/v1/auth/token/refresh/': 'Returns new access and refresh JWT tokens for a user.',
            'api/v1/auth/token/blacklist/': 'Blacklists JWT refresh token for a user.',
            'api/v1/auth/test': 'Returns success if user has proper JWT authorization.',
            'api/v1/auth/create-user/': 'Attemps to create a user in the database.',
            'api/v1/auth/update-user/': 'Attemps to update a user in database.',
        }
        return Response(routes)
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class TestAuth(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response('success')
    
class CreateUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        context = request.data

        response = dict()
        response['success'] = True
        response['errors'] = []

        try:
            user = User.objects.get(email=context['email'])
            response['success'] = False
            response['errors'].append('This email is already registered with a user. Please login.')
        except User.DoesNotExist:
            pass

        try:
            user = User.objects.get(username=context['username'])
            response['success'] = False
            response['errors'].append('Username already exists. Please choose another.')
        except User.DoesNotExist:
            pass
        
        if response['success']:
            user = User.objects.create_user(
                first_name = context['first'],
                last_name = context['last'],
                username = context['username'],
                email = context['email'],
                password = context['password'],
            )
            if context['is_landlord']:
                Landlord.objects.create(user=user)
            else:
                Tenant.objects.create(user=user)
        
        return Response(response)

class UpdateUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        context = request.data
        
        response = dict()
        response['success'] = True
        response['errors'] = []

        user = User.objects.get(id=context['key'])
        user.first_name = context['first']
        user.last_name = context['last']

        if user.email != context['email']:
            try:
                other_user = User.objects.get(email=context['email'])
                response['success'] = False
                response['errors'].append('This email is already registered with a user. Please choose another.')
            except User.DoesNotExist:
                user.email = context['email']


        if user.username != context['username']:
            try:
                other_user = User.objects.get(username=context['username'])
                response['success'] = False
                response['errors'].append('Username already exists. Please choose another.')
            except User.DoesNotExist:
                user.username = context['username']
        
        if response['success']:
            user.save()

        return Response(response)
    
class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        key = request.data['key']

        user = User.objects.get(id=key)

        user.delete()

        return Response({ 'success': True })

