from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User
from django.db import IntegrityError


from user_auth.models import Profile, Landlord, Tenant
from .serializers import MyTokenObtainPairSerializer


class GetRoutes(APIView):
    def get(self, request):
        routes = {
            'api/v1/auth/routes/': 'Returns all api routes for authentication and authorization.',
            'api/v1/auth/token/': 'Returns login access and refresh JWT tokens for a user.',
            'api/v1/auth/token/refresh/': 'Returns new access and refresh JWT tokens for a user.',
            'api/v1/auth/token/blacklist/': 'Blacklists JWT refresh token for a user.',
            'api/v1/auth/test': 'Returns success if user has proper JWT authorization.',
            'api/v1/auth/create-user/': 'Attemps to create a user in the database.'
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
        try:
            user = User.objects.create_user(
                first_name = context['first'],
                last_name = context['last'],
                username = context['username'],
                email = context['email'],
                password = context['password'],
            )
            profile = Profile.objects.create(user=user)
            if context['is_landlord']:
                Landlord.objects.create(profile=profile)
            else:
                Tenant.objects.create(profile=profile)
            return Response({ 'success': True, 'message': 'Signup successful'})
        except IntegrityError as e:
            return Response({ 'success': False, 'message': 'Username already exists. Please choose another.'})
