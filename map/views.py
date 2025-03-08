from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Prefetch

from rest_framework.permissions import IsAuthenticated

from map.serializers import ProjectConnectionsSerializer, ProjectSerializer, UserProjectMapSerializer
from map.models import ProjectMap, ProjectPosition 
# Create your views here.


class ProjectConnectionListAPIView(generics.ListAPIView):
    queryset = ProjectMap.objects.all()
    serializer_class = ProjectConnectionsSerializer
    

class MapElementsView(generics.ListAPIView):
    queryset = ProjectPosition.objects.filter(project__is_limited=False).select_related('project') 
    #select_relatred для жадной загрузки за один раз весь project
    serializer_class = ProjectSerializer
    #permission_classes = [IsAuthenticated]

class UserProjectMapView(generics.ListAPIView):
    queryset = ProjectMap.objects.all().select_related('project')
    serializer_class = UserProjectMapSerializer
    permission_classes = [IsAuthenticated]




# class ProjectConnectionAPIView(APIView):
#     def get(self, request):
#         connections = ProjectMap.objects.all()
#         serializer = ProjectMapSerializer(connections, many=True)
#         return Response({'post': serializer.data})


# class ProjectConnectionViewSet(viewsets.ModelViewSet):
#     queryset = ProjectMap.objects.all()
#     serializer_class = ProjectMapModelSerializer