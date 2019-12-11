from django.urls import path
from core.views import *

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

urlpatterns = [
    path('project_list/', ProjectList.as_view()),
    path('project_list/<int:pk>/', ProjectDetail.as_view()),
    path('task_comments/', TaskCommentList.as_view()),
    path('task_comments/<int:pk>/', TaskCommentDetail.as_view()),
    path('task_documents/', TaskDocumentList.as_view()),
    path('task_documents/<int:pk>/', TaskDocumentDetail.as_view()),
]

router = routers.DefaultRouter()
router.register('project_members', ProjectMemberViewSet, base_name='main')
router.register('tasks', TaskViewSet, base_name='main')
router.register('users', UserViewSet, base_name='main')
router.register('projects', ProjectViewSet, base_name='main')
router.register('task_comments_viewset', TaskCommentViewSet, base_name='main')
urlpatterns += router.urls