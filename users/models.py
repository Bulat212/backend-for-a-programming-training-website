from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    description = models.TextField(verbose_name='Описание проекта', blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)
    coins = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'  # Вход по email
    REQUIRED_FIELDS = ['username']  # Username обязателен, но не используется для логина

    class Meta:
        verbose_name = 'User'
        #verbose_name_plural = 'Users'


