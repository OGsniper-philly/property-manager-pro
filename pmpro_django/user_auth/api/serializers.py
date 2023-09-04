from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serialize JWT access token with custom claims.

    When a user logs in, JWT access and refresh tokens are returned. The access token can be
    decoded to reveal user information. This serializer adds user data to this token.
    """
    @classmethod
    def get_token(cls, user):
        """Get access token and add custom user claims to it."""
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['is_landlord'] = user.is_landlord
        # ...

        return token