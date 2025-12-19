from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, pagination
from rest_framework.decorators import action
from .models import Doaa, Category
from .serializers import DoaaSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import DoaaFilter

# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = pagination.PageNumberPagination

class DoaaViewSet(viewsets.ModelViewSet):
    queryset = Doaa.objects.all().order_by('order', '-created_at')
    serializer_class = DoaaSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = DoaaFilter

    @action(detail=False, methods=['get'], url_path='category/(?P<category_name>[^/.]+)')
    def get_by_category(self, request, category_name=None):
        category = get_object_or_404(Category, name=category_name)
        queryset = Doaa.objects.filter(category=category).order_by('order', '-created_at')
        page = self.paginate_queryset(queryset)
        serializer = DoaaSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)   
