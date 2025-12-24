from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'pdfs', PdfViewSet, basename='pdf')

urlpatterns = [
    path('', include(router.urls)),
]
