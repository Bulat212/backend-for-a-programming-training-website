from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    description = models.TextField(verbose_name='Описание проекта', blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)
    coins = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'User'
        #verbose_name_plural = 'Users'


