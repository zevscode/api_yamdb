from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TokenObtainView, UserRegistrationView,
    UsersViewSet, CategoryViewSet
)

router = DefaultRouter()
router.register('users', UsersViewSet)
router.register('categories', CategoryViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenObtainView.as_view()),
    path('v1/auth/email/', UserRegistrationView.as_view()),
]
