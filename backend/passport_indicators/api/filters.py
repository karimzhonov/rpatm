import django_filters.rest_framework as filters
from ..models import DataTable


class DataTableFilter(filters.FilterSet):
    region = filters.BaseInFilter()
    criteria = filters.CharFilter(method='filter_criteria')
    file = filters.BaseInFilter()

    class Meta:
        model = DataTable
        fields = "__all__"

    def filter_criteria(self, queryset, name, value):
        return queryset.filter(criteria__name=value)