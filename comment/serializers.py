
from ast import TypeVarTuple

from users.models import UserProject
from .models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Comment
        fields = ['user', 'text']


class ProjectCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    project = serializers.CharField(source='project.name')
    user_project = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProject
        fields = ['user', 'project', 'user_project', 'code', 'earned_stars', 'comments']

    def get_user_project(self, obj):
        user_project = Comment.objects.filter(user_project=obj).first()
        return f"{user_project.user_project.pk}"
    
    def get_comments(self, obj):
        comments = Comment.objects.filter(user_project=obj)
        return CommentSerializer(comments, many=True).data
