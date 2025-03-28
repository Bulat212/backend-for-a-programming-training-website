from pyexpat import model
from tkinter import CASCADE
from django.db import models

from project.models import Project
from users.models import User, UserProject

# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_project = models.ForeignKey(UserProject, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user} - {self.user_project} - {self.text[:10]}"
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
