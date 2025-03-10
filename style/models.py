from pyexpat import model
from unicodedata import category
from xml.etree.ElementInclude import default_loader
from django.db import models

from users.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Style(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Стиль'
        verbose_name_plural = 'Стили'


class UserStyle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if(self.is_active):
            UserStyle.objects.filter(
                user=self.user, 
                style__category=self.style.category, 
                is_active=True
            ).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Стиль пользователя'
        verbose_name_plural = 'Стили пользователя'

    def __str__(self):
        return f"{self.user} - {self.style} - {self.style.category}"
