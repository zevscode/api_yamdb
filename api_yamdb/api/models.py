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


# Заглушка для работоспособности модели Rewiew.
# Потом нужно заменить нормальной моделью.
class Title(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Review(models.Model):
    RATING_RANGE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )

    text = models.TextField()
    pub_date = models.DateTimeField(
        "date published",
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews_authors"
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    score = models.IntegerField(
        choices=RATING_RANGE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['-pub_date']
