from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegionView, CriteriaView, UploadView, DataTableView
)

router = DefaultRouter()
router.register('region', RegionView, '')
router.register('criteria', CriteriaView, '')
router.register('upload', UploadView, '')
router.register('data-table', DataTableView, '')


urlpatterns = [
    path('', include(router.urls))
]