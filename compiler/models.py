from tabnanny import verbose
from django.db import models

from project.models import Language, Project
from users.models import User

# Create your models here.

class CodeExecution(models.Model):
    LANGUAGE_CHOICES = [ 
     ('python', 'Python'), 
     ('javascript', 'JavaScript'), 
     ('java', 'Java'), 
     ('cpp', 'C++'), 
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    code = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    input_data = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Компилятор'
        verbose_name_plural = 'Компиляторы'

    def __str__(self):
        return f"{self.user} - {self.project} - date:{self.created_at}"

class Test(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    input_data = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return f"{self.project.name} - input_data: \"{self.input_data}\" - output:\"{self.output}\""