from django.urls import path
from user_app.api.views import registration_view, logout_view, PublicObtainAuthToken

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # For Token Authentication 
    path('login/', PublicObtainAuthToken.as_view(), name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    #For JWT Authentication
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

