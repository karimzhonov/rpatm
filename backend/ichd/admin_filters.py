from django.contrib.admin import filters
from django.utils.translation import gettext_lazy as _
from .models import Criteria, Uploads, Region, Sector, Area


class CriteriaParentFilter(filters.SimpleListFilter):
    title = _('Parent Criteria')
    parameter_name = 'criteria'

    def lookups(self, request, model_admin):
        return Criteria.objects.filter(parent__isnull=True).order_by('order').values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent_id=self.value())
        return queryset


class FileFilter(filters.SimpleListFilter):
    title = _('Uploaded File')
    parameter_name = 'file'

    def lookups(self, request, model_admin):
        return Uploads.objects.order_by('date').values_list('id', 'name')

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.filter(file_id=self.value())


class RegionFilter(filters.SimpleListFilter):
    title = _('Region')
    parameter_name = 'region'

    def lookups(self, request, model_admin):
        return Region.objects.order_by('name').values_list('id', 'name')

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.filter(region_id=self.value())


class SectorFilter(filters.SimpleListFilter):
    title = _('Sector')
    parameter_name = 'sector'

    def lookups(self, request, model_admin):
        return Sector.objects.order_by('number').values_list('id', 'number')

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.filter(sector_id=self.value())


class AreaFilter(filters.SimpleListFilter):
    title = _('Area')
    parameter_name = 'area'

    def lookups(self, request, model_admin):
        return Area.objects.order_by('name').values_list('id', 'name')

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.filter(area_id=self.value())


class ModelCriteriaParentFilter(CriteriaParentFilter):
    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.filter(criteria__parent_id=self.value())
