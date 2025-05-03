
from ast import TypeVarTuple
from tkinter.messagebox import RETRY

from requests import ReadTimeout

from comment.utils import get_user_nickname
from users.models import UserProject
from users.utils import build_photo_url
from .models import Comment
from rest_framework import serializers
from app import settings

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    nickname_id = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['user', 'nickname_id', 'photo', 'text']
    
    # тут obj - объект Comment и ник берется у пользователя привязанного к Comment
    def get_nickname_id(self, obj):
        return get_user_nickname(self, obj)
    
    def get_photo(self, obj):
        users_photo = self.context.get('users_with_photo', None)
        if not users_photo:
            return None
             
        user_photo = users_photo.filter(id=obj.user.id).first()
        if not user_photo:
            return None
        return build_photo_url(user_photo.photo, self, obj)


class ProjectCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    project = serializers.CharField(source='project.name')
    photo = serializers.SerializerMethodField()
    nickname_id = serializers.SerializerMethodField()
    user_project = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProject
        fields = ['user', 'project', 'photo','nickname_id', 'user_project', 'code', 'earned_stars', 'comments']

    def get_comments(self, obj):
        comments = Comment.objects.filter(user_project=obj)
        return CommentSerializer(comments, many=True, context=self.context).data

    def get_user_project(self, obj):
        user_project = UserProject.objects.filter(project=obj.project, user=obj.user).values_list('pk', flat=True).first()
        return user_project
        # if user_project:
        #     return f"{user_project.pk}"
        # return None

    # тут obj - объект UserProject и ник берется у пользователя привязанного к UserProject
    def get_nickname_id(self, obj):
        return get_user_nickname(self, obj)
    
    def get_photo(self, obj):
        
        users_photo = self.context.get('users_with_photo', None)
        if not users_photo:
            return None
            
        user_photo = users_photo.filter(id=obj.user.id).first()
        if not user_photo:
            return None
        return build_photo_url(user_photo.photo, self, obj)
        
        # if not user_photo:
        #     return None

        # request = self.context.get('request')
        # if request:
        #     return request.build_absolute_uri(f"{settings.MEDIA_URL}{user_photo}")
    
        # return f"{settings.MEDIA_URL}{user_photo}"

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
    

class WriteCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['user', 'user_project', 'text']