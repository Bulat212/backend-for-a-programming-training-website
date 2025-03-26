from dataclasses import field
from urllib import request
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from traitlets import default

from project.models import Language
from project.serializers import LastProjectSerializer
from style.models import Category, Style, UserStyle

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
        fields = ['username', 'coins', 'stars', 'photo', 'nickname_id']
        
    def get_nickname_id(self, obj):
        user = self.context['request'].user
        user_style = UserStyle.objects.filter(user=user, style__category__id=2, is_active=True).first()
        if user_style:
            return user_style.style.id
        return 0
    

class ProfileSerializer(serializers.ModelSerializer):
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
    user__id = serializers.IntegerField()
    user__username = serializers.CharField()
    total_experience = serializers.IntegerField()


class UserRankingStarsSerializer(serializers.Serializer):
    user__id = serializers.IntegerField()
    user__username = serializers.CharField()
    total_stars = serializers.IntegerField()



class UserExpGraphSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    class Meta:
        model = UserProgress
        fields = ['user', 'experience', 'date']


class UserSkillsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    language = serializers.SlugRelatedField(slug_field='name', queryset=Language.objects.all(), required=True)
    experience = serializers.IntegerField(required=True)

    class Meta:
        model = UserSkill
        fields = ['user', 'language', 'experience']