from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework.filters import SearchFilter

from .filters import TitlesFilter
from .mixins import CLDViewSet
from .models import Category, Genres, Titles, Review, Comment

from .permissions import IsModerator, IsOwner, IsSuperUser, IsSuperUserOrReadOnly
from .serializers import (
    TokenObtainSerializer, UserRegistrationSerializer,
    UserSerializer, CategorySerializer, GenresSerializer,
    TitlesSerializer, TitlesListSerializer,
    CommentSerializer, ReviewSerializer)

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-pk')
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsSuperUser]

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated],
            serializer_class=UserSerializer)
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(CreateAPIView):
    serializer_class = TokenObtainSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(CLDViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'
    permission_classes = (IsSuperUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = {SearchFilter}
    search_fields = ['name']


class GenresViewSet(CLDViewSet):
    serializer_class = GenresSerializer
    queryset = Genres.objects.all()
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'
    permission_classes = (IsSuperUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']


class TitlesViewSet(viewsets.ModelViewSet):
    serializer_class = TitlesSerializer
    queryset = Titles.objects.all()
    lookup_url_kwarg = 'titles_id'
    permission_classes = (IsSuperUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesListSerializer
        return TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(
            Titles, pk=self.kwargs['title_id']
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(
                Titles, pk=self.kwargs.get('title_id'))
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review, pk=self.kwargs['review_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(
                Review, pk=self.kwargs.get('review_id'))
        )
