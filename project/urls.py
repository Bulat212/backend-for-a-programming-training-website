from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import *

# app_name = 'projects'

router_project = SimpleRouter()
router_user = SimpleRouter()
router_user.register(r'projects', ProjectViewSet, basename="project")
router_project.register(r'user-projects', UserProjectViewSet, basename="user-project")

urlpatterns = [
    
    path('', projects, name='list'),
    path('', include(router_user.urls)),
    path('', include(router_project.urls)),
    path('temporary-projects/', TemporaryProjectsView.as_view()),
    path('started-projects/', StartedProjectsView.as_view()),
    path('finished-projects/', FinishedProjectsView.as_view()),
    
    # path('api/v1/', ProjectViewSet.as_view({'get': 'list'})),
    # path('api/v1/<int:pk>/', ProjectViewSet.as_view({'put': 'update'})),
]

