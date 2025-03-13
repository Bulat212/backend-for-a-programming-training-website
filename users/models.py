from django.db import models
from django.contrib.auth.models import AbstractUser

from project.models import Language, Project
# from style.models import Style

class User(AbstractUser):
    email = models.EmailField(unique=True)
    description = models.TextField(verbose_name='Обо мне', blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True)
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
        verbose_name = 'User'
        #verbose_name_plural = 'Users'


class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='user_projects')
    is_completed = models.BooleanField(default=False)
    code = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    earned_stars = models.IntegerField(default=0)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_projects')
    finished_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Userproject'
        #verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.user.username} - {self.project}"
    
