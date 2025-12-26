import django_filters
from .models import ContactMessage, ViewLog

class ContactMessageFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()
    subject = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ContactMessage
        fields = ['subject', 'created_at', 'replied_at']

class ViewLogFilter(django_filters.FilterSet):
    timestamp = django_filters.DateFromToRangeFilter()
    model_name = django_filters.CharFilter(field_name='content_type__model')

    class Meta:
        model = ViewLog
        fields = ['timestamp', 'model_name']
