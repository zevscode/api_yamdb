from django.urls import path, include
from rest_framework import routers

from .views import CategoryViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
