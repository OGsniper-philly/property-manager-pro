from django.urls import path

from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import GetRoutes, MyTokenObtainPairView, TestAuth, CreateUser


urlpatterns = [
    path('routes/', GetRoutes.as_view(), name='get_routes'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('test/', TestAuth.as_view()),
    path('create-user/', CreateUser.as_view())
]