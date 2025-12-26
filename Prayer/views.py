from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, generics, mixins, pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Video, Pdf
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategorySerializer, VideoSerializer, PdfSerializer
from .filters import VideoFilter, PdfFilter
from accounts.permissions import IsStaffOrReadOnly
from rest_framework import permissions
# Create your views here.

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [permissions.IsAuthenticated, IsStaffOrReadOnly]

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('order', '-created_at')
    serializer_class = VideoSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = VideoFilter
    permission_classes = [permissions.IsAuthenticated, IsStaffOrReadOnly]

class PdfViewSet(viewsets.ModelViewSet):
    queryset = Pdf.objects.all().order_by('order', '-created_at')
    serializer_class = PdfSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PdfFilter
    permission_classes = [permissions.IsAuthenticated, IsStaffOrReadOnly]
