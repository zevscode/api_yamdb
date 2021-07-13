from django.db import models


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
