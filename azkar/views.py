from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, pagination
from rest_framework.decorators import action
from .models import Azkar, Category
from .serializers import AzkarSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AzkarFilter
# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
    
class AzkarViewSet(viewsets.ModelViewSet):
    queryset = Azkar.objects.all().order_by('order', '-created_at')
    serializer_class = AzkarSerializer
    pagination_class = pagination.PageNumberPagination

    @action(detail=False, methods=['get'], url_path='category/(?P<category_content>[^/.]+)')
    def get_by_category(self, request, category_content=None):
        category = get_object_or_404(Category, category=category_content)
        queryset = Azkar.objects.filter(category=category).order_by('order')
        page = self.paginate_queryset(queryset)
        serializer = AzkarSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)