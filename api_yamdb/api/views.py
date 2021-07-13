from rest_framework.filters import SearchFilter

from api_yamdb.api.mixins import CRLViewSet
from api_yamdb.api.models import Category
from api_yamdb.api.serializers import CategorySerializer


class CategoryViewSet(CRLViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_url_kwarg = 'slug'
    filter_backends = {SearchFilter}
    search_fields = ['name']
