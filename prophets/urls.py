from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProphetList, ProphetDetail, VideoViewSet, PdfViewSet

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'pdfs', PdfViewSet, basename='pdfs')

urlpatterns = [
    path('material/', include(router.urls)),
    path('', ProphetList.as_view(), name='prophet-list'),
    path('<int:pk>/', ProphetDetail.as_view(), name='prophet-detail'),
]