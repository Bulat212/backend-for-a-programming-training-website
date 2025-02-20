from django.contrib import admin
from django.urls import include, path

from .views import *


app_name = 'projects'

urlpatterns = [
    
    path('', projects, name='list'),
    # path('<int:project_id>/', views.project_detail, name='detail'),
    path('api/v1/', ProjectAPIList.as_view()),
    # path('api/v1/<int:pk>/', ProjectAPIList.as_view()),
]

