from pyclbr import Class
from django.db import transaction
from rest_framework import serializers
from django.db.models import Q

import project
from project.views import projects
from users.models import UserProject

from .models import ProjectMap, ProjectPosition
from project.models import Project

# class ProjectMapSerializer(serializers.Serializer):
#     project_id= serializers.IntegerField( allow_null=True)
#     prev_project_id = serializers.IntegerField(allow_null=True)  # Получаем ID предыдущего проекта


class ProjectConnectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMap
        fields = ["project", "prev_project"]  #поля которые будут возвращаться по запросу


class ProjectPositionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='project.name')
    description = serializers.CharField(source='project.description')
    experience = serializers.IntegerField(source='project.experience')
    coins = serializers.IntegerField(source='project.coins')
    project_id = serializers.IntegerField(source='project.id')

    class Meta:
        model = ProjectPosition
        fields = ["project_id", "position_x", "position_y", "name", "description", "experience", "coins"]  #поля которые будут возвращаться по запросу

class AdminProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name"]

class UserProjectMapSerializer(serializers.ModelSerializer):
    # project = ProjectSerializer(source='project.positions.first')
    project_id = serializers.IntegerField(source='project.id')
    is_open = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = ProjectMap
        fields = ["project_id", "is_open", "is_completed"]  #поля которые будут возвращаться по запросу

    def get_is_open(self, obj):
        user = self.context['request'].user
        if not obj.prev_project:
            return True
        prev_project_map = ProjectMap.objects.filter(project=obj.prev_project).first()
        if prev_project_map:
            completed = UserProject.objects.filter(user=user, project=prev_project_map.project, is_completed=True).exists()
            if completed:
                return True
        return False

    def get_is_completed(self, obj):
        user = self.context['request'].user
        return UserProject.objects.filter(user=user, project=obj.project, is_completed=True).exists()


class AddMapProjects(serializers.ModelSerializer):
    project_id = serializers.IntegerField()
    prev_project_id = serializers.IntegerField(required=False, allow_null=True)
    position_x = serializers.FloatField(write_only=True)
    position_y = serializers.FloatField(write_only=True)

    class Meta:
        model = ProjectMap
        fields = ['project_id', 'prev_project_id', 'position_x', 'position_y']

    def create(self, validated_data):

        project_id = validated_data.pop('project_id')
        prev_project_id = validated_data.pop('prev_project_id', None)
        position_x = validated_data.pop('position_x')
        position_y = validated_data.pop('position_y')

        project = Project.objects.get(id=project_id)
        prev_project = Project.objects.get(id=prev_project_id) if prev_project_id else None

        new_map_project, created = ProjectMap.objects.update_or_create(project=project, defaults={'prev_project': prev_project})
        ProjectPosition.objects.update_or_create(project=project, defaults={'position_x': position_x, 'position_y': position_y})

        return new_map_project
    
    def validate(self, data):
        project_id=data.get('project_id')
        prev_project_id=data.get('prev_project_id')

        if not Project.objects.filter(id=project_id).exists():
            raise serializers.ValidationError(f"Проект с id={project_id} не найден.")
        
        if prev_project_id and not Project.objects.filter(id=prev_project_id).exists():
            raise serializers.ValidationError(f"Предыдущий проект с id={prev_project_id} не найден.")

        return data


class AddMapProjectsListSerializer(serializers.ListSerializer):
    def create(self, validated_data_list):
        with transaction.atomic():
            ProjectMap.objects.all().delete()
            ProjectPosition.objects.all().delete()

            created_objects = []
            for validated_data in validated_data_list:
                serializer = AddMapProjects(data=validated_data)
                serializer.is_valid(raise_exception=True)
                created_objects.append(serializer.save())

        return created_objects


class AddMapProjectsSerializer(AddMapProjects):
    class Meta(AddMapProjects.Meta):
        list_serializer_class = AddMapProjectsListSerializer