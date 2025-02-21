from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import SimpleRouter, DefaultRouter

from .views import *

app_name = 'projects'

router = DefaultRouter()
router.register(r'projectapi', ProjectViewSet, basename="project")
print(router.urls)

urlpatterns = [
    
    path('', projects, name='list'),
    path('api/', include(router.urls)),

    # path('api/v1/', ProjectViewSet.as_view({'get': 'list'})),
    # path('api/v1/<int:pk>/', ProjectViewSet.as_view({'put': 'update'})),
]

