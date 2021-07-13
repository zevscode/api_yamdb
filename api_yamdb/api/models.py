from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLES = [
        ('user', 'user'),
        ('admin', 'admin'),
        ('moderator', 'moderator'),
    ]
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(
        max_length=9,
        choices=USER_ROLES,
        default='user',
    )
    bio = models.TextField(blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('role',)


class UserRegistration(models.Model):
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=16)



class Category(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Имя категории',
        help_text='Дайте короткое название категории'
    )
    slug = models.SlugField(
        unique=True, verbose_name='Адрес категории',
        help_text=('Если это поле останется пустым '
                   'оно заполнется автоматически')
    )
