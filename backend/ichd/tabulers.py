from django.contrib import admin
from .utils import OnlyShowPermissionMixin
from .models import (AreaTable, AreaTableCriteria, DataTable,
                     RegionSectorTable, RegionSectorTableCriteria, RegionTable,
                     RegionTableCriteria, SectorTable, SectorTableCriteria)


class SectorTableTabularAdmin(OnlyShowPermissionMixin, admin.TabularInline):
    model = SectorTableCriteria
    ordering = ['criteria__order']


class AreaTableTabularAdmin(OnlyShowPermissionMixin, admin.TabularInline):
    model = AreaTableCriteria


class RegionTableTabularAdmin(OnlyShowPermissionMixin, admin.TabularInline):
    model = RegionTableCriteria


class RegionSectorTableTabularAdmin(OnlyShowPermissionMixin, admin.TabularInline):
    model = RegionSectorTableCriteria


class UploadSectorTableTabularAdmin(OnlyShowPermissionMixin, admin.TabularInline):
    model = SectorTable
    ordering = ['order']


class UploadRegionTableTabularAdmin(OnlyShowPermissionMixin, admin.TabularInline):
    model = RegionTable
    show_change_link = True


class UploadRegionSectorTabularAdmin(OnlyShowPermissionMixin, admin.TabularInline):
    model = RegionSectorTable


class UploadAreaTableTabularAdmin(OnlyShowPermissionMixin, admin.TabularInline):
    model = AreaTable


class UploadDataTableTabularAdmin(OnlyShowPermissionMixin, admin.TabularInline):
    model = DataTable
