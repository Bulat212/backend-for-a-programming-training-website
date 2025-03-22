from dataclasses import field
from django.utils import timezone
from rest_framework import serializers
from project.models import Language, Project
from users.models import UserProject

class ProjectSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Project
        #fields=("slug", "name", "description") #поля которые будут возвращаться по запросу
        fields="__all__" #поля которые будут возвращаться по запросу
    

class UserProjectSerializer(serializers.ModelSerializer):
    # project_id = serializers.IntegerField(source='project.id')
    language = serializers.SlugRelatedField(slug_field='name', queryset=Language.objects.all(), required=False)
    project_id = serializers.PrimaryKeyRelatedField(source='project', queryset=Project.objects.all())
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = UserProject
        fields = ['project_id', 'project_name', 'code', 'is_completed', 'is_published', 'earned_stars', 'language', 'finished_date']


class TemporaryProjects(serializers.ModelSerializer):
    time_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'theory', 'time_remaining', 'experience', 'difficulty', 'coins']

    def get_time_remaining(self, obj):
        if obj.time_to_leave < timezone.now():
            return "Время истекло"
        remeaning = obj.time_to_leave - timezone.now()
        days = remeaning.days
        hours, remainder  = divmod(remeaning.seconds, 3600)
        minutes, seconds = divmod(remainder , 60)
        return f"Оставшееся время - {days} дней, {hours} часов, {minutes} минут."
   
   
   
   
    # def create(self, validated_data):
    #     # Извлекаем project_id из данных
    #     project_id = validated_data.pop('project')['id']  # Берем ID из вложенного словаря
    #     project = Project.objects.get(id=project_id)
    #     user_project = UserProject.objects.create(project=project, **validated_data)
    #     return user_project
    

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