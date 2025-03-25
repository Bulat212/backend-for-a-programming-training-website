from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import generics


from users.models import UserProgress
from users.utils import get_experiece_ranking

from .serializers import ProfileSerializer, RegisterSerializer, UserExpGraphSerializer, UserMinInfoSerializer, UserRankingExperienceSerializer, UserRankingStarsSerializer

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


class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
    

class UserExpGraphView(generics.ListAPIView):
    serializer_class = UserExpGraphSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)


class ExperienceRatingView(APIView):
    def get(self, request, period, limit):
        users = get_experiece_ranking("experience", period, limit)
        serializer = UserRankingExperienceSerializer(users, many=True)
        
        return Response(serializer.data)


class StarsRatingView(APIView):
    def get(self, request, period, limit):
        users = get_experiece_ranking("stars", period, limit)
        serializer = UserRankingStarsSerializer(users, many=True)
        
        return Response(serializer.data)

# class WeeklyRankngView(APIView):
#     def get(self, request):
#         one_week_ago = timezone.now() - timedelta(days=7)
#         users = User.objects.values('id', 'username').annotate(
#             earned_experience=Coalesce(Sum('userprogress__experience', filter=Q(userprogress__date__gte=one_week_ago)), Value(0)),
#             earned_stars=Coalesce(Sum('userprogress__stars', filter=Q(userprogress__date__gte=one_week_ago)), Value(0))
#         ).order_by('-earned_experience', '-earned_stars')

#         return Response(list(users))




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