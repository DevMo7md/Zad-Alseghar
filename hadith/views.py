from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Video, Pdf
from .serializers import VideoSerializer, PDFSerializer
from rest_framework import pagination
from django_filters.rest_framework import DjangoFilterBackend 
from .filters import VideoFilter, PdfFilter
from accounts.permissions import IsStaffOrReadOnly
from rest_framework import permissions
# Create your views here.

class HadithVideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('order', '-created_at')
    serializer_class = VideoSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = VideoFilter
    permission_classes = [permissions.IsAuthenticated, IsStaffOrReadOnly]


class HadithPDFViewSet(viewsets.ModelViewSet):
    queryset = Pdf.objects.all().order_by('order', '-created_at')
    serializer_class = PDFSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PdfFilter
    permission_classes = [permissions.IsAuthenticated, IsStaffOrReadOnly]
