from lzma import FORMAT_ALONE
from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from comment.serializers import CommentSerializer, ProjectCommentSerializer
from users.models import UserProject

from .models import Comment
# Create your views here.



class CommentListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectCommentSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return UserProject.objects.filter(project=pk, is_published=True)
        

