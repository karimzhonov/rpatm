from django.db.models.functions import JSONObject
from django.db.models import OuterRef, F, Subquery, Count, Q, Avg
from django.contrib.postgres.expressions import ArraySubquery
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet
from ichd.models import (
    SectorTable, RegionTable, AreaTable, Criteria, RegionSectorTable, Uploads, Area, DataTable,
    RegionTableCriteria, RegionSectorTableCriteria, SectorTableCriteria, Region, AreaTableCriteria, RegionDataTable
    )

from .serializers import HomeSectorChartSerializer, CityCriteriaTableSerializer, SectorRegionBarChartSerializer, PrimaryDataTableSerializer, RegionDataTableSerializer
from .filters import RegionSectorTableFilter, DataTableFilter


@extend_schema_view(list=extend_schema(tags=['ichd_chart'], parameters=[OpenApiParameter('file', str, 'query')]))
class HomeSectorChartView(ReadOnlyModelViewSet):
    serializer_class=HomeSectorChartSerializer

    def get_queryset(self):
        files = self.request.query_params.get('file')
        filter_kwargs = {}
        upload_kwargs = {}
        if files:
            filter_kwargs['file_id__in'] = files.split(',')
            upload_kwargs['id__in'] = files.split(',')
        
        return SectorTable.objects.filter(**filter_kwargs).annotate(
            index=Subquery(SectorTableCriteria.objects.filter(table_id=OuterRef('id'), criteria__main=True).values('index')),
            delta_index=Subquery(SectorTableCriteria.objects.filter(table_id=OuterRef('id'), criteria__main=True).values('delta'))
        ).order_by('sector__number').values(
            'order', 'sector', 'index', 'delta_index',
            area_info=JSONObject(
                min_count=Subquery(
                    AreaTable.objects.filter(
                        sector_id=OuterRef('sector_id'), areatablecriteria__criteria__main=True, **filter_kwargs, areatablecriteria__index__lt=0.55
                        ).values('sector').annotate(count=Count('id')).values('count')[:1]
                ),
                center_count=Subquery(
                    AreaTable.objects.filter(
                        sector_id=OuterRef('sector_id'), areatablecriteria__criteria__main=True, **filter_kwargs, areatablecriteria__index__gte=0.55, areatablecriteria__index__lt=0.65
                        ).values('sector').annotate(count=Count('id')).values('count')[:1]
                ),
                max_count=Subquery(
                    AreaTable.objects.filter(
                        sector_id=OuterRef('sector_id'), areatablecriteria__criteria__main=True, **filter_kwargs, areatablecriteria__index__gte=0.65
                        ).values('sector').annotate(count=Count('id')).values('count')[:1]
                ),
            ),
            bar=JSONObject(
                labels=ArraySubquery(
                    Region.objects.all().order_by('name').values_list('name', flat=True)
                ),
                datasets=ArraySubquery(
                    Uploads.objects.filter(**upload_kwargs).order_by('-date').values(
                        json=JSONObject(
                            id=F('id'),
                            name=F('name'),
                            data=ArraySubquery(
                                RegionSectorTable.objects.filter(
                                    sector_id=OuterRef(OuterRef('sector_id')),
                                    file_id=OuterRef('id')
                                ).annotate(
                                    index=Subquery(
                                            RegionSectorTableCriteria.objects.filter(table_id=OuterRef('id'), criteria__main=True).order_by('criteria__order').values('index')
                                        )
                                ).order_by('region__name').values_list("index", flat=True)
                            )
                        )
                        
                    )
                )
            )
        )
    

@extend_schema_view(list=extend_schema(tags=['ichd_chart'], parameters=[OpenApiParameter('file', str, 'query')]))
class HomeCityDataView(ViewSet):

    def list(self, request, *args, **kwargs):
        files = request.query_params.get('file')
        filter_kwargs = {}
        kwargs = {}
        if files:
            filter_kwargs['file_id__in'] = files.split(',')
            kwargs['table__file_id__in'] = files.split(',')

        return Response({
                "criteria": CityCriteriaTableSerializer(AreaTableCriteria.objects.filter(table__file__status='finished', **kwargs).values('criteria').annotate(
                    index=Avg('index', filter=Q(criteria_id=F('criteria')))).order_by('criteria__order'), many=True).data,
                "area_info": {
                    "min_count": AreaTable.objects.filter(areatablecriteria__criteria__main=True, **filter_kwargs, areatablecriteria__index__lt=0.55).count(),
                    "center_count": AreaTable.objects.filter(areatablecriteria__criteria__main=True, **filter_kwargs, areatablecriteria__index__gte=0.55, areatablecriteria__index__lt=0.65).count(),
                    "max_count": AreaTable.objects.filter(areatablecriteria__criteria__main=True, **filter_kwargs, areatablecriteria__index__gte=0.65).count(),
                }
            })


@extend_schema_view(list=extend_schema(tags=['ichd_chart'], parameters=[OpenApiParameter('file', str, 'query')]))
class SectorRegionBarChartView(ReadOnlyModelViewSet):
    filterset_class = RegionSectorTableFilter
    serializer_class = SectorRegionBarChartSerializer

    def get_queryset(self):
        files = self.request.query_params.get('file')
        filter_kwargs = {}
        upload_kwargs = {}
        if files:
            filter_kwargs['file_id__in'] = files.split(',')
            upload_kwargs['id__in'] = files.split(',')
        
        return RegionSectorTable.objects.annotate(
            labels=ArraySubquery(
                    Criteria.objects.filter(parent__isnull=True, main=False).order_by('order').values_list('name', flat=True)
                ),
            datasets=ArraySubquery(
                    Uploads.objects.filter(**upload_kwargs).order_by('-date').values(
                        json=JSONObject(
                            id=F('id'),
                            name=F('name'),
                            data=ArraySubquery(
                                RegionSectorTableCriteria.objects.filter(table_id=OuterRef(OuterRef('id')), criteria__parent__isnull=True, criteria__main=False).order_by('criteria__order').values('index'),
                        )
                    )
                        
                )
            )
        )


@extend_schema_view(get=extend_schema(tags=['ichd_chart'], parameters=[OpenApiParameter('file', str, 'query'), OpenApiParameter('parent_criteria', str, 'query')]))
class PrimaryDataTableView(ListAPIView):
    serializer_class = PrimaryDataTableSerializer

    def get_queryset(self):
        filter_kwargs = {}
        kwargs = {}
        files = self.request.query_params.get('file')
        parent_criteria = self.request.query_params.get('parent_criteria')
        sector = self.request.query_params.get('sector')
        region = self.request.query_params.get('region')

        if files:
            filter_kwargs['file_id__in'] = files.split(',')

        if parent_criteria:
            filter_kwargs['criteria__parent_id__in'] = parent_criteria.split(',')

        if sector:
            filter_kwargs['sector_id__in'] = sector.split(',')
            kwargs['sector_id__in'] = sector.split(',')

        if region:
            filter_kwargs['region_id__in'] = region.split(',')
            kwargs['region_id__in'] = region.split(',')
        
        
        return Area.objects.filter(**kwargs).annotate(
            data=ArraySubquery(DataTable.objects.filter(**filter_kwargs, area_id=OuterRef('id')).order_by('criteria__order', 'criteria__name').values(json=JSONObject(
                index=F('index'),
                criteria_name=F('criteria__name')
            ))
            )
        )


@extend_schema_view(get=extend_schema(tags=['ichd_chart'], parameters=[OpenApiParameter('file', str, 'query'), OpenApiParameter('parent_criteria', str, 'query')]))
class RegionDataView(ListAPIView):
    serializer_class = RegionDataTableSerializer

    def get_queryset(self):
        filter_kwargs = {}
        files = self.request.query_params.get('file')
        parent_criteria = self.request.query_params.get('parent_criteria')
        if files:
            filter_kwargs['file_id__in'] = files.split(',')

        if parent_criteria:
            filter_kwargs['criteria__parent_id__in'] = parent_criteria.split(',')

        return Region.objects.annotate(
            data=ArraySubquery(RegionDataTable.objects.filter(**filter_kwargs, region_id=OuterRef('id')).order_by('criteria__order', 'criteria__name').values(json=JSONObject(
                index=F('index'),
                criteria_name=F('criteria__name')
                ))
            )
        )
