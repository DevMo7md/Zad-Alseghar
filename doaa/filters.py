import django_filters
from .models import Doaa

class DoaaFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter(field_name='created_at')
    updated_at = django_filters.DateFromToRangeFilter(field_name='updated_at')

    class Meta:
        model = Doaa
        fields = ['category', 'title', 'content', 'created_at', 'updated_at']
