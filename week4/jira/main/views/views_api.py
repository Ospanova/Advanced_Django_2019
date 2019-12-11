from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Project
from main.serializers import ProjectSerializerGet, ProjectSerializerCreateUpdate
from main.response import send_response
from rest_framework import status as status_codes
from django.shortcuts import get_object_or_404


class ProjectListAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializerGet(projects, many=True)
        return send_response(message='All projects', data=serializer.data)

    def post(self, request):
        serializer = ProjectSerializerCreateUpdate(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return send_response(message='Project created', status=status_codes.HTTP_201_CREATED, data=serializer.data)
        return send_response(message=Response(serializer.errors), status=status_codes.HTTP_400_BAD_REQUEST,
                             success=False)


class ProjectDetailAPIView(APIView):
    http_method_names = ['get', 'put', 'delete']

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializerGet(data=project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializerCreateUpdate(instance=project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response(status=status_codes.HTTP_204_NO_CONTENT)
