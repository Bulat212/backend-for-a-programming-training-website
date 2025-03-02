from rest_framework import serializers

import project
from users.models import UserProject

from .models import ProjectMap, ProjectPosition


# class ProjectMapSerializer(serializers.Serializer):
#     project_id= serializers.IntegerField( allow_null=True)
#     prev_project_id = serializers.IntegerField(allow_null=True)  # Получаем ID предыдущего проекта


class ProjectConnectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMap
        fields = ["project", "prev_project"]  #поля которые будут возвращаться по запросу


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='project.name')
    description = serializers.CharField(source='project.description')
    experience = serializers.IntegerField(source='project.experience')
    coins = serializers.IntegerField(source='project.coins')
    project_id = serializers.IntegerField(source='project.id')

    class Meta:
        model = ProjectPosition
        fields = ["project_id", "position_x", "position_y", "name", "description", "experience", "coins"]  #поля которые будут возвращаться по запросу


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
