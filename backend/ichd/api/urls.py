from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ichd.api.views import UploadsView, SectorView, RegionView, AreaView, CriteriaView, SectorTableView, \
    RegionTableView, RegionSectorTableView, AreaTableView, DataTableView

from .chart_views import (HomeSectorChartView, HomeCityDataView, SectorRegionBarChartView, PrimaryDataTableView, RegionDataView)


router = DefaultRouter()
router.register('uploads', UploadsView, '')
router.register('sector', SectorView, '')
router.register('region', RegionView, '')
router.register('area', AreaView, '')
router.register('criteria', CriteriaView, '')
router.register('sector-table', SectorTableView, '')
router.register('region-table', RegionTableView, '')
router.register('region-sector-table', RegionSectorTableView, '')
router.register('area-table', AreaTableView, '')
router.register('data-table', DataTableView, '')

router.register('home-sector-chart', HomeSectorChartView, '')
router.register('home-city-data', HomeCityDataView, '')
router.register('sector-region-bar-chart', SectorRegionBarChartView, '')

urlpatterns = [
    path('', include(router.urls)),
    path('area-data/', PrimaryDataTableView.as_view()),
    path('region-data/', RegionDataView.as_view())
]
