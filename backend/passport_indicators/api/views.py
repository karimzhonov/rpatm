from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import (
    UploadSerializer, RegionSerializer, CriteriaSerializer, DataTableSerializer
)
from ..models import (
    Uploads, Criteria, Region, DataTable
)
from .filters import DataTableFilter


class UploadView(ReadOnlyModelViewSet):
    serializer_class = UploadSerializer
    authentication_classes = ()
    permission_classes = ()

    def get_queryset(self):
        return Uploads.objects.filter(status='finished').order_by('-date')


class RegionView(ReadOnlyModelViewSet):
    serializer_class = RegionSerializer
    authentication_classes = ()
    permission_classes = ()
    search_fields = ('name',)

    def get_queryset(self):
        return Region.objects.all().order_by('name')


class CriteriaView(ReadOnlyModelViewSet):
    serializer_class = CriteriaSerializer
    authentication_classes = ()
    permission_classes = ()
    search_fields = ('name',)

    def get_queryset(self):
        return Criteria.objects.all().order_by('name')


class DataTableView(ReadOnlyModelViewSet):
    serializer_class = DataTableSerializer
    authentication_classes = ()
    permission_classes = ()
    search_fields = ('criteria__name',)
    filterset_class = DataTableFilter

    def get_queryset(self):
        return DataTable.objects.filter(file__status='finished').order_by('criteria__name')
