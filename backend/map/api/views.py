from rest_framework.viewsets import ReadOnlyModelViewSet

from ichd.api.filters import AreaTableFilter
from ichd.api.serializers import AreaTableSerializer
from ichd.models import AreaTable


class AreaDataView(ReadOnlyModelViewSet):
    serializer_class = AreaTableSerializer
    filterset_class = AreaTableFilter
    permission_classes = ()
    authentication_classes = ()

    def get_queryset(self):
        return AreaTable.objects.filter(file__status='finished')
