from rest_framework import serializers
from .models import Doaa, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class DoaaSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Doaa
        fields = ['id', 'title', 'content', 'order', 'category', 'category_id', 'created_at', 'updated_at']
