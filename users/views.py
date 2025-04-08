from django.core.serializers import serialize
from django.db.models import Sum
from django.shortcuts import render
from django.templatetags.i18n import language
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins


from project.models import Language
from users.models import ProgressLog, User, UserProgress, UserSkill

from users.utils import get_ranking, update_or_create_user_skill

from .serializers import ProfileSerializer, RegisterSerializer, UserExpGraphSerializer, UserMinInfoSerializer, UserRankingExperienceSerializer, UserRankingStarsSerializer, UserSkillsSerializer

# Create your views here.
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = serializer.get_tokens(user)
        return Response(tokens, status=status.HTTP_201_CREATED)


class UserMinInfoView(APIView):
    serializer_class = UserMinInfoSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserMinInfoSerializer(user, context={'request': request})
        return Response(serializer.data)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get("id", None)
        if user_id:
            try:
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise Response({"error": "Пользователь с таким id не найден."})
        return self.request.user
    
    def update(self, request):
        user = request.user
        
        username_data = request.data.get('username', None)
        if username_data and User.objects.filter(username=username_data).exists():
            return Response({"error": "Username уже занят."})
        
        serializer = ProfileSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        


    # def get(self, request):
    #     user = request.user
    #     serializer = ProfileSerializer(user)
    #     return Response(serializer.data)
    

class UserExpGraphView(generics.ListAPIView):
    serializer_class = UserExpGraphSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)


class ExperienceRatingView(APIView):
    def get(self, request, period, limit):
        current_user = request.user if request.user.is_authenticated else None
        users = get_ranking("experience", period, limit, current_user)

        curret_user_serializer = UserRankingExperienceSerializer(users['current_user'], context={'request': request}) if current_user else None
        users_serializer = UserRankingExperienceSerializer(users['users'], many=True, context={'request': request})
        return Response({'users': users_serializer.data, 'current_user_ranking':curret_user_serializer.data if current_user else None})


class StarsRatingView(APIView):
    def get(self, request, period, limit):
        current_user = request.user if request.user.is_authenticated else None
        users = get_ranking("stars", period, limit, current_user)
        
        curret_user_serializer = UserRankingStarsSerializer(users['current_user'], context={'request': request}) if current_user else None
        users_serializer = UserRankingStarsSerializer(users['users'], many=True, context={'request': request})
        return Response({'users': users_serializer.data, 'current_user_ranking':curret_user_serializer.data if current_user else None})

        # serializer = UserRankingStarsSerializer(users, many=True, context={'request': request})
        
        # return Response(serializer.data)


class UserSkillsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        all_languages = Language.objects.all()

        user_skills = UserSkill.objects.filter(user=request.user)
        
        languages_with_zero_experience = []
        if not user_skills.exists():
            for lang in all_languages:
                new_lang = {}
                new_lang["language"] = lang.name
                new_lang["experience"] = 0
                languages_with_zero_experience.append(new_lang)

            return Response(languages_with_zero_experience)
        
        user_skill_serializer = UserSkillsSerializer(user_skills, many=True).data
        
        user_languages =[]
        for skill in user_skill_serializer:
            user_languages.append(skill['language'])
        
        for language in all_languages:
            if language.name not in user_languages:
                user_skill_serializer.append({'language':language.name, 'experience':0})
        
        return Response(user_skill_serializer)

    def post(self, request):
        serializer = UserSkillsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        language_name = request.data.get('language')
        experience = request.data.get('experience')

        language = Language.objects.get(name = language_name)
        user_skill= update_or_create_user_skill(user, language, experience)

        serializer = UserSkillsSerializer(user_skill) #передаем просто объект user_skill,
        # валидировать и сохранять не нужно, без data= потому что передаем объект, а не словарь
        return Response(serializer.data)



# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)