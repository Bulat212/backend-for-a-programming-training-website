from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import *


app_name = 'projects'

router = SimpleRouter()
router.register(r'projectapi', ProjectViewSet)

urlpatterns = [
    
    path('', projects, name='list'),
    path('', include(router.urls)),

    # path('api/v1/', ProjectViewSet.as_view({'get': 'list'})),
    # path('api/v1/<int:pk>/', ProjectViewSet.as_view({'put': 'update'})),
]

