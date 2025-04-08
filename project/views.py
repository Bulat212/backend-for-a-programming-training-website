from time import timezone
from tkinter import NO
from django.core.serializers import serialize
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from project.models import Language, Project
from project.serializers import ProjectSerializer, StatusUserProject, TemporaryProjects, UserProjectSerializer
from users.models import UserProject
from map.models import ProjectMap
from users.utils import update_user_progress
from compiler.utils import run_tests

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
    
    # @action(methods=['get'], detail=True) #True одна запись, False список
    # def language(self, request, pk):
    #     language = Language.objects.get(pk=pk)
    #     return Response({'post': language.name})

class UserProjectViewSet(viewsets.ModelViewSet):
    serializer_class = UserProjectSerializer
    permission_classes = [IsAuthenticated]
    # http_method_names = ['get']  # Разрешаем только GET

    def get_queryset(self):
        return UserProject.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        project_id = self.kwargs['pk']  # Используем pk как project_id
        obj = get_object_or_404(queryset, project=project_id)  # Ищем по project_id
        return obj

    def perform_create(self, serializer): #Автоматически добавляет user при создании записи.
        serializer.save(user=self.request.user)

    def update(self, request, pk=None):
        user_project = self.get_object()
        allowed_fields = {
            key: value for key, value in request.data.items()
            if key in ['code', 'is_published', 'earned_stars', 'language']
        }
        serializer = self.get_serializer(user_project, data=allowed_fields, partial=True) #partial частичное обновление
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


    # ставит статус выполнен и текущее время
    @action(methods=['put'], detail=True)
    def end_project(self, request, pk=None):
        user_project = self.get_object()  # Получаем объект по pk
        if user_project.is_completed:
            return Response({'detail': 'Проект уже завершен'}, status=400)
        
        project = Project.objects.get(id=pk)

        result_tests = run_tests(user_project.code, user_project.language, project)
        if result_tests['status']==False:
            return Response({"Project completion status": "Failed"})
         
        update_user_progress(request.user, project.experience)
        
        user_project.finished_date = timezone.now()
        user_project.is_completed = True
        user_project.save(update_fields=['finished_date', 'is_completed'])
        serializer = self.get_serializer(user_project)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def get_user_project(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.validated_data['project']

        user_project = UserProject.objects.filter(user=self.request.user, project=project).first()
        if user_project:
            serializer = self.get_serializer(instance=user_project, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        
        # if UserProject.objects.filter(user=self.request.user, project=project).exists():
        #     return Response({'detail': 'Проект уже начат'}, status=400)
        
        if project.is_limited==False:
            project_map = ProjectMap.objects.filter(project=project).first()
            if project_map and project_map.prev_project:
                prev_user_project = UserProject.objects.filter(user=self.request.user, project=project_map.prev_project).first()
                if not prev_user_project:
                    return Response({'detail': 'Проект начать нельзя: предыдущий проект еще не начат'}, status=400)
                if prev_user_project.is_completed==False:
                    return Response({'detail': 'Проект начать нельзя: предыдущий проект не завершен'}, status=400)

        self.perform_create(serializer)
        return Response(serializer.data)


    
class TemporaryProjectsView(generics.ListAPIView):
    serializer_class = TemporaryProjects
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(
            is_limited=True,
            time_to_leave__gt=timezone.now()
        )


class StartedProjectsView(generics.ListAPIView):
    serializer_class = StatusUserProject
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        return UserProject.objects.filter(user=self.request.user, is_completed=False)
    

class FinishedProjectsView(generics.ListAPIView):
    serializer_class = StatusUserProject
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        return UserProject.objects.filter(user=self.request.user, is_completed=True)
    


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