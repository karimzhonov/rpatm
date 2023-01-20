from django.db.models import OuterRef, F, Subquery
from django.db.models.functions import JSONObject
from django.contrib.postgres.expressions import ArraySubquery
from rest_framework.viewsets import ReadOnlyModelViewSet

from ichd.api.filters import AreaTableFilter
from .serializers import AreaTableSerializer
from ichd.models import AreaTable, DataTable, Uploads


class AreaDataView(ReadOnlyModelViewSet):
    serializer_class = AreaTableSerializer
    filterset_class = AreaTableFilter
    permission_classes = ()
    authentication_classes = ()

    def get_queryset(self):
        criteria = [
            'Аҳоли сони', 'Оилалар сони', 'МТМ қамров даражаси', 'Мактаблар қамров даражаси', '	7-17 ёшдаги болалар сони',
            'Cодир этилган жиноятлар сони', 'Ўғирлик', 'Безорилик', 'Номусга тегиш', 'Иқтисодий фаол аҳоли сони', 'Ишсизлар сони',
            'Ёшлар (18-30 ёшдаги) ишсизлар сони', 'Аҳоли жон бошига реал даромад (минг сўм)', 'Ёшлар дафтари', 'Аёлар дафтари',
            'Темир дафтар', 'Алимент тўламаётганлар сони', 'Уйга муҳтож аҳоли сони',
        ]
        kwargs = {}
        file_list = self.request.query_params.get('file', '0').split(',')
        if file_list == ['0']:
            kwargs['file_id'] = Subquery(
                Uploads.objects.filter(status='finished').order_by('-date')[:1].values('id')
            )
        else:
            kwargs['file_id__in'] = file_list
        return AreaTable.objects.filter(file__status='finished').annotate(
            criteria=ArraySubquery(
                DataTable.objects.filter(
                    area_id=OuterRef('area_id'), criteria__name__in=criteria, **kwargs
                    ).order_by('criteria__name').values(json=JSONObject(
                        criteria=F('criteria__name'),
                        index=F('index'),
                    ))
            )
        )
