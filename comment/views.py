from lzma import FORMAT_ALONE
from shutil import register_unpack_format
from django.core.serializers import serialize
from django.http import QueryDict
from django.shortcuts import render

from django.template import context
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from comment.serializers import CommentSerializer, ProjectCommentSerializer, SetLikeInCodeSerializer
from users.models import UserProject

from .models import Comment, Like
# Create your views here.



class CommentListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectCommentSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return UserProject.objects.filter(project=pk, is_published=True)
        

class SetLikeInUserProjectView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        liker = request.user
        
        project = request.data.get('user_project_id')
        user_project = UserProject.objects.filter(pk=project).first()
        
        if not user_project:
            return Response({"error": "Проект не найден."})

        if user_project.user.username == liker.username:
            return Response({"error": "Нельзя самому себе ставить лайки."})
        
        if Like.objects.filter(user=liker, project=user_project).exists():
            return Response({"error":"Нельзя повторно ставить лайки."})

        Like.objects.create(user=liker, project=user_project)
        user_project.earned_stars += 1
        user_project.save()
        serializer = SetLikeInCodeSerializer(user_project, context={'liker': liker})
        return Response({"message": f"Лайк добавлен на {user_project}.", "data": serializer.data})






