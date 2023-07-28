from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import MyTokenObtainPairSerializer


class GetRoutes(APIView):
    def get(self, request):
        routes = {
            'api/v1/auth/routes/': 'Returns all api routes for authentication and authorization.',
            'api/v1/auth/token/': 'Returns login access and refresh JWT tokens for a user.',
            'api/v1/auth/token/refresh/': 'Returns new access and refresh JWT tokens for a user.',
            'api/v1/auth/token/blacklist/': 'Blacklists JWT refresh token for a user.',
            'api/v1/auth/test': 'Returns success if user has proper JWT authorization.'
        }
        return Response(routes)
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class TestAuth(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response('success')