from logging.config import valid_ident
from lzma import FORMAT_ALONE
from shutil import register_unpack_format
from sys import is_stack_trampoline_active
from django.core.serializers import serialize
from django.http import QueryDict
from django.shortcuts import render

from django.template import context
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


from comment.permissions import IsAdminOrOwner
from comment.serializers import CommentSerializer, ProjectCommentSerializer, SetLikeInCodeSerializer, WriteCommentSerializer
from style.models import UserStyle
from users.models import User, UserProject
from users.utils import update_user_progress

from .models import Comment, Like
# Create your views here.



class CommentListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectCommentSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return UserProject.objects.filter(project=pk, is_published=True).select_related('project', 'user')
    
    def get_serializer_context(self):
        # Добавляем дополнительные данные в контекст сериализатора
        context = super().get_serializer_context()
        context['users_nickname'] = UserStyle.objects.filter(is_active=True, style__category=2)
        context['users_with_photo'] = User.objects.filter(photo__isnull=False).exclude(photo='')

        return context
    
class CommentDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAdminOrOwner]


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
        update_user_progress(user_project.user, None, 0, 0, 1)
        serializer = SetLikeInCodeSerializer(user_project, context={'liker': liker})
        return Response({"message": f"Лайк добавлен на {user_project}.", "data": serializer.data})


class WriteCommentAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WriteCommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

        