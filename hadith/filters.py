import django_filters
from .models import Video, Pdf

class VideoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Video
        fields = ['title', 'description', 'created_at']

class PdfFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Pdf
        fields = ['title', 'created_at']
