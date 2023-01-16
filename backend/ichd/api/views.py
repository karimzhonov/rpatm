from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Avg, F, Q
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from ichd.api.filters import SectorTableFilter, RegionTableFilter, RegionSectorTableFilter, AreaTableFilter, \
    DataTableFilter, CriteriaFilter, UploadFilter, CityCriteriaFilter
from ichd.api.serializers import UploadSerializer, SectorSerializer, RegionSerializer, AreaSerializer, \
    CriteriaSerializer, SectorTableSerializer, RegionTableSerializer, RegionSectorTableSerializer, AreaTableSerializer, \
    DataTableSerializer, CityCriteriaTableSerializer
from ichd.models import Uploads, Sector, Region, Area, Criteria, SectorTable, RegionTable, RegionSectorTable, AreaTable, \
    DataTable, AreaTableCriteria


class UploadsView(ReadOnlyModelViewSet):
    serializer_class = UploadSerializer
    filterset_class = UploadFilter

    def get_queryset(self):
        return Uploads.objects.filter(status='finished')


class SectorView(ReadOnlyModelViewSet):
    serializer_class = SectorSerializer

    def get_queryset(self):
        return Sector.objects.all()


class RegionView(ReadOnlyModelViewSet):
    serializer_class = RegionSerializer
    search_fields = ['name']

    def get_queryset(self):
        return Region.objects.all()


class AreaView(ReadOnlyModelViewSet):
    serializer_class = AreaSerializer

    def get_queryset(self):
        return Area.objects.all()


class CriteriaView(ReadOnlyModelViewSet):
    serializer_class = CriteriaSerializer
    filterset_class = CriteriaFilter
    search_fields = ['name']

    def get_queryset(self):
        return Criteria.objects.all().order_by('order', 'name')


class SectorTableView(ReadOnlyModelViewSet):
    serializer_class = SectorTableSerializer
    filterset_class = SectorTableFilter

    def get_queryset(self):
        return SectorTable.objects.filter(file__status='finished').order_by('sector__number')


class RegionTableView(ReadOnlyModelViewSet):
    serializer_class = RegionTableSerializer
    filterset_class = RegionTableFilter

    def get_queryset(self):
        return RegionTable.objects.filter(file__status='finished')


class RegionSectorTableView(ReadOnlyModelViewSet):
    serializer_class = RegionSectorTableSerializer
    filterset_class = RegionSectorTableFilter

    def get_queryset(self):
        return RegionSectorTable.objects.filter(file__status='finished')


class AreaTableView(ReadOnlyModelViewSet):
    serializer_class = AreaTableSerializer
    filterset_class = AreaTableFilter

    def get_queryset(self):
        return AreaTable.objects.filter(file__status='finished')


class DataTableView(ReadOnlyModelViewSet):
    serializer_class = DataTableSerializer
    filterset_class = DataTableFilter

    def get_queryset(self):
        return DataTable.objects.filter(file__status='finished').order_by('criteria__order')


class CityCriteriaTableView(ReadOnlyModelViewSet):
    serializer_class = CityCriteriaTableSerializer
    filterset_class = CityCriteriaFilter

    def get_queryset(self):
        return AreaTableCriteria.objects.filter(table__file__status='finished')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.values('criteria').annotate(
            index=Avg('index', filter=Q(criteria_id=F('criteria')))).order_by('criteria__order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
