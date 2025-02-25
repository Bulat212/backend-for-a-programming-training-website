from rest_framework import serializers
from traitlets import default

from .models import ProjectMap, ProjectPosition


# class ProjectMapSerializer(serializers.Serializer):
#     project_id= serializers.IntegerField( allow_null=True)
#     prev_project_id = serializers.IntegerField(allow_null=True)  # Получаем ID предыдущего проекта

    
class ProjectMapModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMap
        fields = ["project", "prev_project"]  #поля которые будут возвращаться по запросу


class MapElementsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='project.name')
    description = serializers.CharField(source='project.description')
    experience = serializers.IntegerField(source='project.experience')
    coins = serializers.IntegerField(source='project.coins')

    class Meta:
        model = ProjectPosition
        fields = ["project_id", "position_x", "position_y", "name", "description", "experience", "coins"]  #поля которые будут возвращаться по запросу

