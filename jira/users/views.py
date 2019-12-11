from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from users.serializers import *

from rest_framework.permissions import IsAuthenticated

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


@api_view(['POST'])
def logout(request):
    request.auth.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def current(request):
    permission_classes = (IsAuthenticated,)
    user = request.user
    print(user)
    return Response(status=status.HTTP_204_NO_CONTENT)