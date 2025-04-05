from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path

from app import settings
from compiler.views import CheckSolutionAPIView, ExecuteCodeView
from project import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [

    # path('admin/', admin.site.urls),
    path('code-executor/',ExecuteCodeView.as_view()),
    path('code-executor/check-solution/', CheckSolutionAPIView.as_view()),

]