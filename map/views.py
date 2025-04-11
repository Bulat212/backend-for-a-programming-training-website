from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Prefetch

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from map.serializers import AddMapProjects, AddMapProjectsSerializer, ProjectConnectionsSerializer, ProjectPositionSerializer, AdminProjectSerializer, UserProjectMapSerializer
from map.models import ProjectMap, ProjectPosition
from project.models import Project 
# Create your views here.


class ProjectConnectionListAPIView(generics.ListAPIView):
    queryset = ProjectMap.objects.all()
    serializer_class = ProjectConnectionsSerializer
    

class MapElementsView(generics.ListAPIView):
    queryset = ProjectPosition.objects.filter(project__is_limited=False).select_related('project') 
    #select_relatred для жадной загрузки за один раз весь project
    serializer_class = ProjectPositionSerializer
    #permission_classes = [IsAuthenticated]

class UserProjectMapView(generics.ListAPIView):
    queryset = ProjectMap.objects.all().select_related('project')
    serializer_class = UserProjectMapSerializer
    permission_classes = [IsAuthenticated]

class AdminProjectListAPIView(generics.ListAPIView):
    queryset = Project.objects.filter(is_limited=False).exclude(id__in=ProjectMap.objects.values('project_id'))
    serializer_class = AdminProjectSerializer
    permission_classes = [IsAdminUser]


class AdminMapCreateAPIView(generics.CreateAPIView):
    serializer_class = AddMapProjectsSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    



# class ProjectConnectionAPIView(APIView):
#     def get(self, request):
#         connections = ProjectMap.objects.all()
#         serializer = ProjectMapSerializer(connections, many=True)
#         return Response({'post': serializer.data})


# class ProjectConnectionViewSet(viewsets.ModelViewSet):
#     queryset = ProjectMap.objects.all()
#     serializer_class = ProjectMapModelSerializer