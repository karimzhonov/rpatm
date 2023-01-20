from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AreaDataView,
)

router = DefaultRouter()
router.register('area-data', AreaDataView, '')

urlpatterns = [
    path('', include(router.urls))
]