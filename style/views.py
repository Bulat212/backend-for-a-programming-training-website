from functools import partial
from gettext import install
from typing import Never
from django.conf.global_settings import SESSION_SAVE_EVERY_REQUEST
from django.core.serializers import get_serializer, serialize
from django.shortcuts import render
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins

from style.models import Style, UserStyle
from style.serializers import StyleSerializer, UserStyleSerializer, UserStyleSetIsActiveSerializer

from users.models import User
# Create your views here.


# class StyleList(generics.ListAPIView):
#     queryset = Style.objects.filter(is_available=True)
#     serializer_class = StyleSerializer

class StyleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='exact')
    
    class Meta:
        model = Style
        fields = {
            'price_in_coin': ['lt', 'gt'],  # Фильтрация по цене (меньше или больше)
            'price_in_stars': ['lt', 'gt'], 
        }


class StyleViewSet(viewsets.ModelViewSet):
    serializer_class = StyleSerializer
    filter_backends= [DjangoFilterBackend]
    filterset_class = StyleFilter

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        if not pk:
            return Style.objects.filter(is_available=True)
        
        return Style.objects.filter(pk=pk)
    

class UserStyleAPIView(generics.ListCreateAPIView):
    # queryset = UserStyle.objects.all()
    serializer_class = UserStyleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserStyle.objects.filter(user=user)

    def perform_create(self, serializer): #Автоматически добавляет user при создании записи.
        serializer.save(user=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserStyleSerializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        style = serializer.validated_data['style']
        
        userstyle_is_exist =  UserStyle.objects.filter(user=self.request.user, style=style).exists()
        if userstyle_is_exist:
            return Response({'detail': 'Этот стиль уже куплен.'}, status=status.HTTP_400_BAD_REQUEST)
        
        currency = serializer.validated_data['currency']
        style_price_coin = style.price_in_coin
        style_price_stars = style.price_in_stars

        shopping_successfull = False

        if currency=="stars":
            user_stars = request.user.stars
            if user_stars >= style_price_stars:
                request.user.stars -= style_price_stars
                request.user.save()
                shopping_successfull = True
        
        if currency == "coins":
            user_coins = request.user.coins
            if user_coins >= style_price_coin:
                request.user.coins -= style_price_coin
                request.user.save()
                shopping_successfull = True
       
        if shopping_successfull:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        else:
            return Response({"detail": "Не хватает средств."}, status=status.HTTP_400_BAD_REQUEST)


class UserStyleSetIsActiveView(generics.UpdateAPIView):
    serializer_class = UserStyleSetIsActiveSerializer
    permission_classes= [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        style_id = kwargs.get("style_id", None)

        if style_id==0:
            category = request.data.get("clear_category")
            if category=="nickname":
                user_style = UserStyle.objects.filter(style__category=2, user=request.user, is_active=True).first()
                if not user_style:
                    return Response({"detail":"У пользователя нет такого активного стиля."})
                else:
                    user_style.is_active = False
            
            elif(category=="background_profile"):
                user_style = UserStyle.objects.filter(style__category=1, user=request.user, is_active=True).first()
                if not user_style:
                    return Response({"detail":"У пользователя нет такого активного стиля."})
                else:
                    user_style.is_active = False

            user_style.save()
            return Response(UserStyleSetIsActiveSerializer(instance = user_style).data)
        
        user_style = UserStyle.objects.filter(style=style_id, user=request.user).first()
        if not user_style:
            return Response({"detail":"У пользователя нет такого стиля."})
        
        user_style.is_active=True
        serializer = UserStyleSetIsActiveSerializer(data = request.data, instance = user_style, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
