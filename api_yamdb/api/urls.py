from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TokenObtainView, UserRegistrationView, UsersViewSet

router = DefaultRouter()
router.register('users', UsersViewSet)


urlpatterns = [
    path('v1/auth/token/', TokenObtainView.as_view()),
    path('v1/auth/email/', UserRegistrationView.as_view()),
    path('v1/', include(router.urls)),
]
