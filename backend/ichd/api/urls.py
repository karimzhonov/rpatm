from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ichd.api.views import UploadsView, SectorView, RegionView, AreaView, CriteriaView, SectorTableView, \
    RegionTableView, RegionSectorTableView, AreaTableView, DataTableView

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

urlpatterns = [
    path('', include(router.urls))
]
