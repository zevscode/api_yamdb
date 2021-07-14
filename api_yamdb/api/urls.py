from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TokenObtainView, UserRegistrationView,
    UsersViewSet, CategoryViewSet, GenresViewSet, TitlesViewSet,
)

router = DefaultRouter()
router.register('users', UsersViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitlesViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenObtainView.as_view()),
    path('v1/auth/email/', UserRegistrationView.as_view()),
]
