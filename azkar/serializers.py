from rest_framework import serializers
from .models import Azkar, Category

class AzkarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Azkar
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'