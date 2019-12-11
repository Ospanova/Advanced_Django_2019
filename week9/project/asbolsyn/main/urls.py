from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()

# router.register('tasks', TaskViewSet, base_name='core')

urlpatterns = router.urls
