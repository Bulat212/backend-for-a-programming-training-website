import re
from wsgiref.util import request_uri
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.decorators import action

from compiler.models import CodeExecution, Test
from compiler.serializers import CodeExecutionSerializer
from compiler.utils import run_tests
import project
from project.models import Language
from users.utils import update_user_progress
from .services.judge0 import execute_code, get_execution_result
import time

LANGUAGE_IDS = {
    "python": 71,
    "javascript": 63,
    "cpp": 54,
    "java": 62
}

class ExecuteCodeView(generics.ListCreateAPIView):     
    queryset = CodeExecution.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CodeExecutionSerializer

    def post(self, request):
        serializer = CodeExecutionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get("code")
        language = serializer.validated_data.get("language")
        input_data = serializer.validated_data.get("input_data", "")
        project_id = serializer.validated_data.get("project")
        user_project = serializer.validated_data.get("user_project")
        
        if language.compiler_name not in LANGUAGE_IDS:
          return Response({"error": "Unsupported language"}, status=400)
        
        token = execute_code(code, LANGUAGE_IDS[language.compiler_name], input_data)
        time.sleep(2)  # Ждем завершения выполнения
        
        # if not token:
        #     Response({"error":"Попытки закончились."})
        
        result = get_execution_result(token)
        output = result.get("stdout") or result.get("stderr")
        
        submission = CodeExecution.objects.create(
            user=self.request.user,
            code=code,
            project=project_id,
            language=language,
            input_data=input_data,
            output=output
        )

        user_project.language = language
        user_project.code = code
        user_project.save()
    
        return Response({
            "output": output,
            "status": result["status"]["description"]
        })
        
    

class CheckSolutionAPIView(APIView):

    def post(self, request):
        serializer = CodeExecutionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get("code")
        language = serializer.validated_data.get("language")
        project = serializer.validated_data.get("project")
        user_project = serializer.validated_data.get("user_project")
        
        user_project.code = code
        user_project.language = language
        user_project.save()
        
        result_tests = run_tests(code, language, project)

        if result_tests['status']==False:
            return Response(result_tests)
        else:
            return Response({"status": True})
        
        # if language.compiler_name not in LANGUAGE_IDS:
        #     return Response({"error": "Unsupported language"}, status=400)
        
        # tests = Test.objects.filter(project=project)

        # for test in tests:
        #     # output = test.input_data.replace('\\n', '\n').rstrip()
        #     # print(output)
        #     # print(test.output)
        #     # print(input_data)
        #     # print("end")
        #     formatted_input= test.input_data.replace('\\n', '\n')
        #     token = execute_code(code, LANGUAGE_IDS[language.compiler_name], formatted_input)
        #     time.sleep(2)  # Ждем завершения выполнения
            
        #     result = get_execution_result(token)

        #     output = result.get("stdout") or result.get("stderr")
        #     formatted_output= output.strip()

        #     if formatted_output != test.output:
        #         return Response({
        #             "output": output,
        #             "status": "Failed",

        #         })

        # return Response({
        #     # "output": output,
        #     "status": result["status"]["description"]
        # })