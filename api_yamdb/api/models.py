from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


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
    name = models.CharField('Имя категории', max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:100]
        super().save(*args, **kwargs)


class Genres(models.Model):
    name = models.CharField('Нзавание жанра', max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:100]
        super().save(*args, **kwargs)


class Titles(models.Model):
    name = models.CharField('Название', max_length=258)
    year = models.IntegerField('Год выпуска', default=0)
    description = models.TextField('Описание', max_length=258)
    category = models.ForeignKey(
        Category, verbose_name='Категории',
        on_delete=models.SET_NULL, null=True
    )
    genre = models.ManyToManyField(Genres, through='GenresTitles')


class GenresTitles(models.Model):
    genres = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True)
    titles = models.ForeignKey(Titles, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.genres} {self.titles}'
