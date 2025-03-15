from django.db import models

from project.models import Project

# Create your models here.
class ProjectMap(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='maps')
    prev_project = models.ForeignKey(to=Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='next_projects')


    class Meta:
        verbose_name = 'Карта проектов'
        verbose_name_plural = 'Карта проектов'
    
    def __str__(self): # в админке будут видны названия проектов иначе ProjectMap object (1)
        return str(self.project)
    

class ProjectPosition(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='positions')
    position_x = models.FloatField()
    position_y = models.FloatField()

    class Meta:
        verbose_name = 'Позиция проекта'
        verbose_name_plural = 'Позиции проектов'
    
    def __str__(self):
        return str(self.project)