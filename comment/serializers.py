
from ast import TypeVarTuple
from tkinter.messagebox import RETRY

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
        user_project = UserProject.objects.filter(project=obj.project, user=obj.user).first()
        if user_project:
            return f"{user_project.pk}"
        return None

    def get_comments(self, obj):
        comments = Comment.objects.filter(user_project=obj)
        return CommentSerializer(comments, many=True).data


class SetLikeInCodeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    earned_stars = serializers.IntegerField(read_only=True)
    liker = serializers.SerializerMethodField(read_only=True)
    project = serializers.CharField(source='project.name')

    class Meta:
        model = UserProject
        fields = ['user', 'project', 'earned_stars', 'liker']

    def get_liker(self, obj):
        liker = self.context.get("liker", None)
        if liker:
            return liker.username
        return None