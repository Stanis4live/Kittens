import django_filters
from exhibition.models import Kitten

class KittenFilterSet(django_filters.FilterSet):
    breed = django_filters.CharFilter(field_name='breed__name', lookup_expr='icontains')
    breed_id = django_filters.NumberFilter(field_name='breed__id', )

    class Meta:
        model = Kitten
        fields = ['breed', 'breed_id']
