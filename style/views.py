from typing import Never
from django.shortcuts import render
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from style.models import Style, UserStyle
from style.serializers import StyleSerializer, UserStyleSerializer

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
