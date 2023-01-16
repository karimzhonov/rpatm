import django_filters.rest_framework as filters
from django.db.models import Subquery
from ichd.models import SectorTable, RegionTable, RegionSectorTable, AreaTable, DataTable, Criteria, Uploads, AreaTableCriteria, Area


class CriteriaFilter(filters.FilterSet):
    not_parent = filters.BooleanFilter(method='filter_not_parent')
    parent = filters.BaseInFilter()

    class Meta:
        model = Criteria
        fields = ['not_parent', 'parent']

    def filter_not_parent(self, queryset, name, value):
        return queryset.filter(parent__isnull=value)


class SectorTableFilter(filters.FilterSet):
    sector = filters.BaseInFilter(method='filter_sector')
    file = filters.BaseInFilter(method='filter_file')
    date_range = filters.CharFilter(method='filter_date_range')

    class Meta:
        model = SectorTable
        fields = ['sector', 'file', 'date_range']

    def filter_sector(self, queryset, name, value):
        return queryset.filter(sector_id__in=value).order_by('file__date')

    def filter_file(self, queryset, name, value):
        if value == ['0']:
            return queryset.filter(file_id=Subquery(queryset.order_by('-file__date')[:1].values('file_id')))
        return queryset.filter(file_id__in=value).order_by('sector__number')

    def filter_date_range(self, queryset, name, value):
        from_at, to_at, *_ = value.split('-')
        return queryset.filter(file__date__year__gte=from_at, file__date__year__lte=to_at).order_by('file__date')


class RegionTableFilter(filters.FilterSet):
    region = filters.BaseInFilter()
    file = filters.BaseInFilter(method='filter_file')
    date_range = filters.CharFilter(method='filter_date_range')

    class Meta:
        model = RegionTable
        fields = ['region', 'file', 'date_range']

    def filter_file(self, queryset, name, value):
        if value == ['0']:
            return queryset.filter(file_id=Subquery(queryset.order_by('-file__date')[:1].values('file_id')))
        return queryset.filter(file_id__in=value)

    def filter_date_range(self, queryset, name, value):
        from_at, to_at, *_ = value.split('-')
        return queryset.filter(file__date__year__gte=from_at, file__date__year__lte=to_at).order_by('file__date')


class RegionSectorTableFilter(filters.FilterSet):
    region = filters.BaseInFilter(method='filter_region')
    sector = filters.BaseInFilter(method='filter_sector')
    file = filters.BaseInFilter(method='filter_file')
    date_range = filters.CharFilter(method='filter_date_range')

    class Meta:
        model = RegionSectorTable
        fields = ['region', 'sector', 'file', 'date_range']

    def filter_file(self, queryset, name, value):
        if value == ['0']:
            return queryset.filter(file_id=Subquery(queryset.order_by('-file__date')[:1].values('file_id')))
        return queryset.filter(file_id__in=value)

    def filter_date_range(self, queryset, name, value):
        from_at, to_at, *_ = value.split('-')
        return queryset.filter(file__date__year__gte=from_at, file__date__year__lte=to_at).order_by('file__date')

    def filter_region(self, queryset, name, value):
        return queryset.filter(region_id__in=value).order_by('sector__number', 'file__date')

    def filter_sector(self, queryset, name, value):
        return queryset.filter(sector_id__in=value).order_by('region__name', 'file__date')


class AreaTableFilter(filters.FilterSet):
    region = filters.BaseInFilter()
    sector = filters.BaseInFilter()
    area = filters.BaseInFilter()
    file = filters.BaseInFilter(method='filter_file')

    class Meta:
        model = AreaTable
        fields = ['area', 'file', 'sector', 'region']

    def filter_file(self, queryset, name, value):
        if value == ['0']:
            return queryset.filter(file_id=Subquery(
                Uploads.objects.filter(status='finished').order_by('-date')[:1].values('id')
            ))
        return queryset.filter(file_id__in=value).order_by('file__date')


class DataTableFilter(filters.FilterSet):
    region = filters.BaseInFilter()
    sector = filters.BaseInFilter()
    area = filters.BaseInFilter()
    file = filters.BaseInFilter()
    parent_criteria = filters.BaseInFilter(method='filter_parent_criteria')
    main_criteria = filters.BooleanFilter(method='filter_main_criteria')
    index_color = filters.CharFilter(method='filter_index_color')

    class Meta:
        model = DataTable
        fields = ['region', 'sector', 'area', 'file', 'parent_criteria']

    def filter_parent_criteria(self, queryset, name, value):
        return queryset.filter(criteria__parent_id__in=value).order_by('file__date', 'criteria__order')

    def filter_main_criteria(self, queryset, name, value):
        return queryset.filter(criteria__main=value).order_by('-index')

    def filter_index_color(self, queryset, name, value):
        ranges = {
            'red': (0, 0.55),
            'blue': (0.55, 0.65),
            'green': (0.65, 1),
        }
        l, g = ranges.get(value, (0, 0))
        return queryset.filter(index__gte=l, index__lt=g)

class UploadFilter(filters.FilterSet):
    id = filters.BaseInFilter()
    region = filters.BaseInFilter(method=lambda queryset, *args: queryset)
    sector = filters.BaseInFilter(method=lambda queryset, *args: queryset)
    area = filters.BaseInFilter(method=lambda queryset, *args: queryset)
    parent_criteria = filters.BaseInFilter(method=lambda queryset, *args: queryset)

    class Meta:
        model = Uploads
        fields = ['id', 'region', 'sector', 'area', 'parent_criteria']


class CityCriteriaFilter(filters.FilterSet):
    file = filters.BaseInFilter(method='filter_file')

    class Meta:
        model = AreaTableCriteria
        fields = ['file']

    def filter_file(self, queryset, name, value):
        return queryset.filter(table__file_id__in=value)