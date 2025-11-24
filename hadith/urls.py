from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'videos', HadithVideoViewSet, basename='video')
router.register(r'pdfs', HadithPDFViewSet, basename='pdf')

urlpatterns = [
    path('', include(router.urls)),
]