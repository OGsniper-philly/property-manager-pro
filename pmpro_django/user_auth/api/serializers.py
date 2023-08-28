from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import User


# Customize token claims here
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        # ...

        return token