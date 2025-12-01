from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AzkarViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'contents', AzkarViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]