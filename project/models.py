from django.db import models

# Create your models here.

class Project(models.Model):
    slug = models.SlugField(max_length=150, unique=True)
    name = models.CharField(max_length=150, unique=True, verbose_name='Название проекта') #verbose для админки
    description = models.TextField(verbose_name='Описание проекта', blank=True)
    theory = models.TextField(verbose_name='Теория', blank=True)
    time_to_leave = models.TimeField(default='00:00:00')
    experience = models.PositiveIntegerField(blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    coins = models.IntegerField(blank=True, null=True)
    created_data = models.DateTimeField(auto_now_add=True)
    is_limited = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
    
    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name

class ProjectLanguage(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='languages')
    language = models.ForeignKey(to=Language, on_delete=models.CASCADE, related_name='projects')

