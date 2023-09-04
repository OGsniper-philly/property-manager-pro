from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

from .views import CreateUser, UpdateUser, DeleteUser


"""
API descriptions:

:route token/: (post) expects username and password, returns JWT access and refresh tokens. Used for login.
:route token/refresh/: (post) expects valid refresh token, returns new JWT access and refresh tokens. Old refresh blacklisted.
:route token/blacklist/: (post) expects valid refresh token, blacklists this token. Used for logout.
:route create-user/: (post) expects signup user data, attempts to create this user in the database.
:route update-user/: (post) expects update user data, attempts to update this user in the database.
:route delete-user/: (post) deletes user who made request from the database.
:route password-reset/: (post) expects user email and sends reset password link. Reset password token included as URL parameter.
"""
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('create-user/', CreateUser.as_view(), name='create_user'),
    path('update-user/', UpdateUser.as_view(), name='update_user'),
    path('delete-user/', DeleteUser.as_view(), name='delete-user'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]