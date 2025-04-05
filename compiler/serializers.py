
import queue
from urllib import request
from rest_framework import serializers

from compiler.models import CodeExecution
from project.models import Project

class CodeExecutionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    code = serializers.CharField(max_length=10000)
    language = serializers.CharField()
    input_data = serializers.CharField(required=False)
    output = serializers.CharField(required=False, read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = CodeExecution
        fields = ['user', 'project', 'code', 'language', 'input_data', 'output', 'created_at']

