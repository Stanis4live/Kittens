import django_filters
from exhibition.models import Kitten

class KittenFilterSet(django_filters.FilterSet):
    breed = django_filters.CharFilter(field_name='breed__name', lookup_expr='icontains')

    class Meta:
        model = Kitten
        fields = ['breed', 'id']
