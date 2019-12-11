from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.models import *
from rest_framework.permissions import *
from rest_framework import viewsets
from rest_framework.decorators import action
from core.serializers import *
from rest_framework import generics
from rest_framework import mixins
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser


class ProjectList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProjectDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskCommentList(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TaskCommentDetail(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskDocumentList(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = TaskDocument.objects.all()
    serializer_class = TaskDocumentSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TaskDocumentDetail(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    queryset = TaskDocument.objects.all()
    serializer_class = TaskDocumentSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectMemberFullSerializer
        return ProjectMemberSerializer

    @action(methods=['GET', 'POST'], detail=True)
    def members(self, request, pk):
        if request.method == 'GET':
            project = Project.objects.get(id=pk)
            projectmembers = project.project_members.all()
            serializer = ProjectMemberSerializer(projectmembers, many=True)
            return Response(serializer.data)
        else:
            project = Project.objects.get(id=pk)
            user = self.request.user
            projectmember = ProjectMember(project=project, user=user)
            projectmember.save()
            serializer = ProjectMemberSerializer(projectmember)
            return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def members_of_my_projects(self, request):
        projectmembers = ProjectMember.members.members_of_my_projects(self.request.user)
        serializer = ProjectMemberFullSerializer(projectmembers, many=True)
        return Response(serializer.data)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectFullSerializer
        return ProjectSerializer

    @action(methods=['GET'], detail=False)
    def myprojects(self, request):
        projects = Project.projects.my_projects(request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.tasks.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskFullSerializer
        return TaskShortSerializer

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f"{self.request.user} created task: {serializer.data.get('name')}")

    @action(methods=['GET'], detail=False)
    def my_tasks(self, request):
        tasks = Task.tasks.my_tasks(self.request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)



class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = TaskComment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskCommentFullSerializer
        return TaskCommentSerializer

    @action(methods=['GET'], detail=True)
    def comments_of_task(self, request, pk):
        task = Task.objects.get(id=pk)
        serializer = TaskCommentSerializer(task.comments, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = MainUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserSerializerFull
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]