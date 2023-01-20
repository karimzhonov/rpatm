from rest_framework import serializers
from ..models import (
    Uploads, Region, Criteria, DataTable
)

class UploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Uploads
        fields = ('id', 'name', 'date')


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = "__all__"


class CriteriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = "__all__"


class DataTableSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    criteria = CriteriaSerializer()
    file = UploadSerializer()

    class Meta:
        model = DataTable
        fields = "__all__"
