from django.urls import path
from rest_framework import routers

from main.views import ProjectListAPIView, \
    ProjectDetailAPIView, BlockListView, BlockDetailView, TaskViewSet, \
    MemberProjectViewSet, TaskDocumentViewSet, TaskCommentViewSet

urlpatterns = [
    path('projects/', ProjectListAPIView.as_view()),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view()),
    path('blocks/', BlockListView.as_view()),
    path('blocks/<int:pk>/', BlockDetailView.as_view()),
]

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet, base_name='main')
router.register('member_projects', MemberProjectViewSet, base_name='main')
router.register('task_documents', TaskDocumentViewSet, base_name='main')
router.register('task_comments', TaskCommentViewSet, base_name='main')

urlpatterns += router.urls
