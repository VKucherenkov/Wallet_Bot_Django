import django_filters
from .models import OperationUser

class OperationUserFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='datetime_add', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='datetime_add', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='operation_type', lookup_expr='exact')
    card = django_filters.CharFilter(field_name='operation_type', lookup_expr='exact')

    class Meta:
        model = OperationUser
        fields = ['category', 'card']  # Поля, по которым можно фильтровать