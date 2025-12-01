import django_filters
from .models import Azkar

class AzkarFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__category', lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter(field_name='created_at')
    updated_at = django_filters.DateFromToRangeFilter(field_name='updated_at')

    class Meta:
        model = Azkar
        fields = ['category', 'created_at', 'updated_at']
