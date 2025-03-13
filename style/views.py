from django.shortcuts import render
from rest_framework import generics

from style.models import Style
from style.serializers import StyleSerializer
# Create your views here.


class StyleList(generics.ListAPIView):
    queryset = Style.objects.filter(is_available=True)
    serializer_class = StyleSerializer