from django.contrib import admin
from compiler.models import CodeExecution, Test

# Register your models here.

admin.site.register(Test)
admin.site.register(CodeExecution)