from dataclasses import field
from http import server
from turtle import position
from urllib import request
from django.db.models import Sum
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from traitlets import default

from app import settings
from project.models import Language
from project.serializers import LastProjectSerializer
from style.models import Category, Style, UserStyle
from users.utils import build_photo_url

from .models import ProgressLog, User, UserProgress, UserProject, UserSkill

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Этот email уже зарегистрирован.'})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
        # return User.objects.create_user(**validated_data)

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
        
class UserMinInfoSerializer(serializers.ModelSerializer):
    nickname_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'coins', 'stars', 'photo', 'nickname_id', 'is_staff']
        
    def get_nickname_id(self, obj):
        user = self.context['request'].user
        user_style = UserStyle.objects.filter(user=user, style__category__id=2, is_active=True).first()
        if user_style:
            return user_style.style.id
        return 0
    

class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False)
    experience = serializers.IntegerField(read_only=True)
    nickname_id = serializers.IntegerField(source='nickname_id.id', default=0, read_only=True)
    background_profile = serializers.IntegerField(source='background_profile.id', default=0, read_only=True)
    last_projects = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'description', 'photo', 'experience', 'nickname_id', 'background_profile', 'last_projects']

    def get_last_projects(self, obj):
        last_projects = UserProject.objects.filter(user=obj, is_completed=True).order_by('-finished_date')[:2]
        return LastProjectSerializer(last_projects, many=True).data


class UserRankingExperienceSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(source='user__id')
    username = serializers.CharField(source='user__username')
    photo = serializers.SerializerMethodField()
    nickname_id = serializers.SerializerMethodField()
    total_experience = serializers.IntegerField(required=False)
    position = serializers.IntegerField(required=False)

    def get_nickname_id(self, obj):
        if not obj['user__nickname_id']:
            return 0
        return obj['user__nickname_id']
    
    def get_photo(self, obj):
        user_photo = obj.get('user__photo')
        return build_photo_url(user_photo, self, obj)
        
        # if not user_photo:
        #     return None
        
        # request = self.context.get('request')
        # if request:
        #     return request.build_absolute_uri(f"{settings.MEDIA_URL}{user_photo}")
        
        # return f"{settings.MEDIA_URL}{user_photo}"


class UserRankingStarsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(source='user__id')
    username = serializers.CharField(source='user__username')
    photo = serializers.SerializerMethodField()
    nickname_id = serializers.SerializerMethodField()
    total_stars = serializers.IntegerField(required=False)
    position = serializers.IntegerField(required=False)
    
    def get_nickname_id(self, obj):
        if not obj['user__nickname_id']:
            return 0
        return obj['user__nickname_id']

    def get_photo(self, obj):
        user_photo = obj.get('user__photo')
        # user_photo = obj.get('user__photo')
        return build_photo_url(user_photo, self, obj)
        
        # if not user_photo:
        #     return None
        
        # request = self.context.get('request')
        # if request:
        #     return request.build_absolute_uri(f"{settings.MEDIA_URL}{user_photo}")
        
        # return f"{settings.MEDIA_URL}{user_photo}"


class UserExpGraphSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    class Meta:
        model = UserProgress
        fields = ['user', 'experience', 'date']


class UserSkillsSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source='user.username', read_only=True)
    language = serializers.SlugRelatedField(slug_field='name', queryset=Language.objects.all(), required=True)
    experience = serializers.IntegerField(required=True)

    class Meta:
        model = UserSkill
        fields = ['language', 'experience']