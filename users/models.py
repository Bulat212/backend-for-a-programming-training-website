from locale import currency
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import time
from django.utils import timezone
from django.db.models import F
from django.db.models import Sum

from project.models import Language, Project
# from style.models import Style

class User(AbstractUser):
    email = models.EmailField(unique=True)
    description = models.TextField(verbose_name='Обо мне', blank=True, null=True)
    photo = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)
    coins = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)
    nickname_id = models.ForeignKey(
        'style.Style',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='nickname_projects'
    )
    background_profile = models.ForeignKey(
        'style.Style',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='background_profile'
    )

    USERNAME_FIELD = 'email'  # Вход по email
    REQUIRED_FIELDS = ['username']  # Username обязателен, но не используется для логина

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='user_projects')
    is_completed = models.BooleanField(default=False)
    code = models.TextField(blank=True, null=True, default=None)
    is_published = models.BooleanField(default=False)
    earned_stars = models.IntegerField(default=0)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_projects')
    finished_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Проект пользователя'
        verbose_name_plural = 'Проекты пользователя'

    def __str__(self):
        return f"{self.user.username} - {self.project}"
    
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)


    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user} - exp:{self.experience} - stars:{self.stars} - {self.date}"
    
    class Meta:
        verbose_name = 'Прогресс пользователя'
        verbose_name_plural = 'Прогресс пользователей'


class ProgressLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experience_change = models.IntegerField(default=0)
    stars_change = models.IntegerField(default=0)  
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - exp:{self.experience_change} - stars:{self.stars_change} - {self.date}"


class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    experience = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Навык пользователя'
        verbose_name_plural = 'Навыки пользователей'

    def __str__(self):
        return f"{self.user} - {self.language} - exp:{self.experience}"


