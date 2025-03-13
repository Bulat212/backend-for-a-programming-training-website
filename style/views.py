from django.shortcuts import render
import django_filters
from rest_framework import generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


from style.models import Style
from style.serializers import StyleSerializer
# Create your views here.


class StyleList(generics.ListAPIView):
    queryset = Style.objects.filter(is_available=True)
    serializer_class = StyleSerializer

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
    