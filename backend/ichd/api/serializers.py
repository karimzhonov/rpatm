from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from ichd.models import (
    Uploads, Sector, Region, Area, Criteria,
    SectorTable, RegionTable, RegionSectorTable, AreaTable,
    DataTable, SectorTableCriteria, RegionSectorTableCriteria, AreaTableCriteria
)


class UploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Uploads
        fields = ('id', 'name', 'date')

    # def get_data(self, obj: Uploads):
    #     request = self.context['request']
    #     sector = request.query_params.get('sector', '').split(',')
    #     region = request.query_params.get('region', '').split(',')
    #     area = request.query_params.get('area', '').split(',')
    #     filter_kwargs = {}
    #     if not sector == ['']:
    #         filter_kwargs['sector_id__in'] = sector
    #     if not region == ['']:
    #         filter_kwargs['region_id__in'] = region
    #     if not area == ['']:
    #         filter_kwargs['area_id__in'] = area
    #     if len(filter_kwargs) > 0:
    #         return DataTableSerializer(obj.datatable_set.filter(**filter_kwargs), many=True, context=self.context).data
    #     return []


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = "__all__"


class SectorTableCriteriaSerializer(serializers.ModelSerializer):
    criteria = CriteriaSerializer()

    class Meta:
        model = SectorTableCriteria
        fields = "__all__"


class SectorTableSerializer(serializers.ModelSerializer):
    sector = SectorSerializer()
    criteria = serializers.SerializerMethodField()
    index = serializers.SerializerMethodField()
    delta_index = serializers.SerializerMethodField()
    file = UploadSerializer()

    class Meta:
        model = SectorTable
        fields = "__all__"

    @extend_schema_field(SectorTableCriteriaSerializer(many=True))
    def get_criteria(self, obj: SectorTable):
        return SectorTableCriteriaSerializer(obj.sectortablecriteria_set.all(), many=True, context=self.context).data

    @extend_schema_field(serializers.FloatField())
    def get_index(self, obj: SectorTable):
        return obj.sectortablecriteria_set.filter(criteria__main=True).order_by('criteria__order').first().index

    @extend_schema_field(serializers.FloatField())
    def get_delta_index(self, obj: SectorTable):
        return obj.sectortablecriteria_set.filter(criteria__main=True).order_by('criteria__order').first().delta


class RegionTableSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = RegionTable
        fields = "__all__"


class RegionSectorTableCriteriaSerializer(serializers.ModelSerializer):
    criteria = CriteriaSerializer()

    class Meta:
        model = RegionSectorTableCriteria
        fields = "__all__"


class RegionSectorTableSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    sector = SectorSerializer()
    criteria = serializers.SerializerMethodField()
    index = serializers.SerializerMethodField()
    delta_index = serializers.SerializerMethodField()
    file = UploadSerializer()

    class Meta:
        model = RegionSectorTable
        fields = "__all__"

    @extend_schema_field(RegionSectorTableCriteriaSerializer(many=True))
    def get_criteria(self, obj: RegionSectorTable):
        return RegionSectorTableCriteriaSerializer(obj.regionsectortablecriteria_set.all(), many=True,
                                                   context=self.context).data

    @extend_schema_field(serializers.FloatField())
    def get_index(self, obj: RegionSectorTable):
        return obj.regionsectortablecriteria_set.filter(criteria__main=True).order_by('criteria__order').first().index

    @extend_schema_field(serializers.FloatField())
    def get_delta_index(self, obj: RegionSectorTable):
        return obj.regionsectortablecriteria_set.filter(criteria__main=True).order_by('criteria__order').first().delta


class AreaTableCriteriaSerializer(serializers.ModelSerializer):
    criteria = CriteriaSerializer()

    class Meta:
        model = AreaTableCriteria
        fields = "__all__"


class AreaTableSerializer(serializers.ModelSerializer):
    area = AreaSerializer()
    region = RegionSerializer()
    sector = SectorSerializer()
    criteria = serializers.SerializerMethodField()
    index = serializers.SerializerMethodField()
    delta_index = serializers.SerializerMethodField()
    file = UploadSerializer()

    class Meta:
        model = AreaTable
        fields = "__all__"

    @extend_schema_field(AreaTableCriteriaSerializer(many=True))
    def get_criteria(self, obj: AreaTable):
        return AreaTableCriteriaSerializer(obj.areatablecriteria_set.all(), many=True,
                                           context=self.context).data

    @extend_schema_field(serializers.FloatField())
    def get_index(self, obj: AreaTable):
        return obj.areatablecriteria_set.filter(criteria__main=True).order_by('criteria__order').first().index

    @extend_schema_field(serializers.FloatField())
    def get_delta_index(self, obj: AreaTable):
        return obj.areatablecriteria_set.filter(criteria__main=True).order_by('criteria__order').first().delta


class DataTableSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    sector = SectorSerializer()
    area = AreaSerializer()
    criteria = CriteriaSerializer()
    file = UploadSerializer()

    class Meta:
        model = DataTable
        exclude = ['index_delta']
