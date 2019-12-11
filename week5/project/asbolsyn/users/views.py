from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import MainUserSerializer
from .models import MainUser


class RegisterAPIView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = MainUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MainUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MainUser.objects.all()
    serializer_class = MainUserSerializer
    permission_classes = (IsAuthenticated,)

    @action(methods=['GET'], detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
