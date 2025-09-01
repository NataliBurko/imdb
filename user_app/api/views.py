from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status

from user_app.api.serializers import RegistrationSerializer


class PublicObtainAuthToken(ObtainAuthToken):
    authentication_classes = []      # login itself doesn’t require token
    permission_classes = [AllowAny]  # open endpoint


@api_view(['POST'])
def logout_view(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data= request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['username'] = account.username
            data['email'] = account.email
        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)
