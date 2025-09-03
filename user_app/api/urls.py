from django.urls import path
from user_app.api.views import registration_view, logout_view, PublicObtainAuthToken

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('login/', PublicObtainAuthToken.as_view(), name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'), 
]

