from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.db.models import Avg
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    UserRegistration, Category, Genres,
    Titles, GenresTitles, Review, Comment
)

User = get_user_model()

class RoleField(serializers.ChoiceField):
    def to_representation(self, value):
        return self._choices[value]

    def to_internal_value(self, data):
        for key, value in self._choices.items():
            if value == data:
                return key
        self.fail('invalid_choice', input=data)


class UserSerializer(serializers.ModelSerializer):
    role = RoleField(choices=User.USER_ROLE_CHOICES)

    class Meta:
        fields = (
            'username', 'email', 'role', 'first_name', 'last_name', 'bio',
        )
        model = User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email',)
        model = UserRegistration

    def save(self):
        email = self.validated_data['email']
        confirmation_code = get_random_string(length=16)
        UserRegistration.objects.create(
            email=email, confirmation_code=confirmation_code
        )
        send_mail(
            'YaMDb Registration',
            f'Your Confirmation Code: {confirmation_code}',
            settings.DEFAULT_FROM_EMAIL,
            (email,)
        )


class TokenObtainSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, write_only=True)
    confirmation_code = serializers.CharField(max_length=16, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email')
        confirmation_code = data.get('confirmation_code')
        registration_record = get_object_or_404(
            UserRegistration, email=email
        )
        if registration_record.confirmation_code == confirmation_code:
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.username = email
                user.save()
            token = RefreshToken.for_user(user)
            return {
                'token': str(token.access_token),
            }
        raise serializers.ValidationError('Wrong Confirmation Code')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genres


class SlugSerializer(serializers.RelatedField):

    def to_internal_value(self, data):
        return data

    def to_representation(self, instance):
        return instance.slug


def genre_get_or_create(titles, genres):
    for genre in genres:
        current_genres, status = Genres.objects.get_or_create(
            slug=genre,
        )
        GenresTitles.objects.get_or_create(
            titles=titles, genres=current_genres
        )
    return genres


class TitlesSerializer(serializers.ModelSerializer):
    genre = SlugSerializer(many=True, queryset=Genres.objects.all())
    category = SlugSerializer(queryset=Category.objects.all())

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)
        read_only_fields = ('id',)
        model = Titles

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        current_category, status = Category.objects.get_or_create(
            slug=validated_data['category']
        )
        validated_data['category'] = current_category
        titles = Titles.objects.create(**validated_data)
        genre_get_or_create(titles, genres)
        return titles

    def update(self, instance, validated_data):
        genres = validated_data.get('genre', None)
        if genres is not None:
            genre_get_or_create(instance, genres)
        category, status_category = Category.objects.get_or_create(
            slug=validated_data.get('category'),
        )
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.category = category
        instance.save()
        return instance


class TitlesListSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField('get_rating')

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )
        read_only_fields = ('id', 'rating',)
        model = Titles

    def get_rating(self, obj):
        ratings = Review.objects.filter(
            title_id=obj.id
        ).aggregate(Avg('score'))
        return ratings['score__avg']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
