from tkinter import NO
from django.core.serializers import serialize
from django.forms import model_to_dict
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, GenericAPIView

from project.models import Language, Project
from project.serializers import ProjectSerializer, UserProjectSerializer
from users.models import UserProject

# Create your views here.

def index(request):
    return HttpResponse("home page")

def about(request):
    return HttpResponse("about page")


def projects(request):
    projects_list = Project.objects.all()

    context = {
        "projects": projects_list,
    }
    return render(request, "project/base.html", context)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     pk = self.kwargs.get("pk")
    #     if not pk:
    #         return Project.objects.all()
    #     return Project.objects.filter(pk=pk)
    
    @action(methods=['get'], detail=True) #True одна запись, False список
    def language(self, request, pk):
        language = Language.objects.get(pk=pk)
        return Response({'post': language.name})

    # @action(methods=['get'], detail=False) #True одна запись, False список
    # def started(self, request, pk):
    #     language = Language.objects.get(pk=pk)
    #     return Response({'post': language.name})

# class UserProjectViewSet(viewsets.ModelViewSet):
#     serializer_class = UserProjectSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return UserProject.objects.filter(user=self.request.user)


# class ProjectAPIDetail(mixins.RetrieveModelMixin,
#                                    mixins.UpdateModelMixin,
#                                    mixins.DestroyModelMixin,
#                                    mixins.CreateModelMixin):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
    

# class ProjectAPIList(generics.ListCreateAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer

# class ProjectAPIUpdate(generics.UpdateAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer

# class ProjectAPIDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer




# class ProjectAPIView(APIView):
#     def get(self, request):
#         project_list = Project.objects.all()
#         return Response({'posts': ProjectSerializer(project_list, many=True).data})
    
#     def post(self, request):
#         serializer = ProjectSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save() 
#         return Response({'post': serializer.data})
    
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({'error': 'Метод PUT не разрешен'})
        
#         try:
#             instance = Project.objects.get(id=pk)
#         except:
#             return Response({'error': 'Проект не найден'})
        
#         serializer = ProjectSerializer(data=request.data, instance=instance) #если тут два параметра,
#         #то save автоматом вызовет update
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'post': serializer.data})
    
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)

#         if not pk:
#             return Response({"error": "Метод DELETE не разрешен"})
        
#         try:
#             project = Project.objects.get(id=pk)
#             project.delete()
#         except:
#             return Response({"error": "Проект не найден"})
        
#         return Response({'post': f'delete post {pk}'})