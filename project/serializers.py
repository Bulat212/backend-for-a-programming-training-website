from rest_framework import serializers
from traitlets import default

from project.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        #fields=("slug", "name", "description") #поля которые будут возвращаться по запросу
        fields="__all__" #поля которые будут возвращаться по запросу

    
    
    
    # slug = serializers.SlugField(required=False)
    # name = serializers.CharField()
    # description = serializers.CharField(required=False)
    # theory = serializers.CharField(required=False)
    # time_to_leave = serializers.TimeField(required=False)
    # experience = serializers.IntegerField(default=0)
    # difficulty = serializers.IntegerField(default=0)
    # coins = serializers.IntegerField(default=0)
    # created_data = serializers.DateTimeField(read_only=True)
    # is_limited = serializers.BooleanField(default=False)

    # def create(self, validated_data):
    #     return Project.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.slug = validated_data.get("slug", instance.slug)
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.description = validated_data.get("description", instance.description)
    #     instance.theory = validated_data.get("theory", instance.theory)
    #     instance.time_to_leave = validated_data.get("time_to_leave", instance.time_to_leave)
    #     instance.experience = validated_data.get("experience", instance.experience)
    #     instance.difficulty = validated_data.get("difficulty", instance.difficulty)
    #     instance.coins = validated_data.get("coins", instance.coins)
    #     instance.created_data = validated_data.get("created_data", instance.created_data)
    #     instance.is_limited = validated_data.get("is_limited", instance.is_limited)
    #     instance.save()
    #     return instance