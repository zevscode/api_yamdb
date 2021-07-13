from rest_framework import serializers

from api_yamdb.api.models import Category


class CategorySerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        fields = ('name', 'slug', 'count', 'next', 'previous', 'results')
        read_only_fields = ('count', 'next', 'previous', 'results')
        model = Category

    def get_count(self, obj):
        return Category.objects.count()

    def get_results(self):
        return Category.objects.all()
