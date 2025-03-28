from django.urls import include, path


from .views import *

urlpatterns = [

    path('comment/<int:pk>/', CommentListAPIView.as_view()),

]

