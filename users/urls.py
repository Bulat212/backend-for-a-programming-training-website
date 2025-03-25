from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import ProfileView, RegisterView, StarsRatingView, UserExpGraphView, UserMinInfoView, ExperienceRatingView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    path('usermininfo/', UserMinInfoView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('user-graph/', UserExpGraphView.as_view()),
    path('experience-ranking/<str:period>/<int:limit>/', ExperienceRatingView.as_view()),
    path('stars-ranking/<str:period>/<int:limit>/', StarsRatingView.as_view()),
    
]

