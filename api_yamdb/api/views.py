from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework.filters import SearchFilter

from .mixins import CRLViewSet
from .models import Category


from .permissions import IsModerator, IsOwner, IsSuperUser
from .serializers import (TokenObtainSerializer, UserRegistrationSerializer,
                          UserSerializer, CategorySerializer)

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



class CategoryViewSet(CRLViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_url_kwarg = 'slug'
    filter_backends = {SearchFilter}
    search_fields = ['name']
