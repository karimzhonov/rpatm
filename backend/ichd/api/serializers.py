from drf_spectacular.utils import extend_schema_field
from ichd.models import (Area, AreaTable, AreaTableCriteria, Criteria,
                         DataTable, Region, RegionSectorTable,
                         RegionSectorTableCriteria, RegionTable,
                         RegionTableCriteria, Sector, SectorTable,
                         SectorTableCriteria, Uploads)
from ichd.utils import intspace
from rest_framework import serializers


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uploads
        fields = ('id', 'name', 'date')


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
        return SectorTableCriteriaSerializer(obj.sectortablecriteria_set.all().order_by('criteria__order'), many=True,
                                             context=self.context).data

    @extend_schema_field(serializers.FloatField())
    def get_index(self, obj: SectorTable):
        return obj.sectortablecriteria_set.filter(criteria__main=True).order_by('criteria__order').first().index

    @extend_schema_field(serializers.FloatField())
    def get_delta_index(self, obj: SectorTable):
        return obj.sectortablecriteria_set.filter(criteria__main=True).order_by('criteria__order').first().delta


class RegionTableCriteriaSerializer(serializers.ModelSerializer):
    criteria = CriteriaSerializer()

    class Meta:
        model = RegionTableCriteria
        fields = "__all__"


class RegionTableSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    criteria = serializers.SerializerMethodField()
    index = serializers.SerializerMethodField()
    delta_index = serializers.SerializerMethodField()
    file = UploadSerializer()

    class Meta:
        model = RegionTable
        fields = "__all__"

    @extend_schema_field(RegionTableCriteriaSerializer(many=True))
    def get_criteria(self, obj: RegionTable):
        return RegionTableCriteriaSerializer(obj.regiontablecriteria_set.all().order_by('criteria__order'), many=True,
                                             context=self.context).data

    @extend_schema_field(serializers.FloatField())
    def get_index(self, obj: Region):
        return obj.regiontablecriteria_set.filter(criteria__main=True).order_by('criteria__order').first().index

    @extend_schema_field(serializers.FloatField())
    def get_delta_index(self, obj: RegionTable):
        return obj.regiontablecriteria_set.filter(criteria__main=True).order_by('criteria__order').first().delta


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
        return RegionSectorTableCriteriaSerializer(obj.regionsectortablecriteria_set.all().order_by('criteria__order'),
                                                   many=True,
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
        return AreaTableCriteriaSerializer(obj.areatablecriteria_set.filter(criteria__main=False).order_by('criteria__order'), many=True,
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


class DataTableShortSerializer(serializers.ModelSerializer):
    criteria = CriteriaSerializer()

    class Meta:
        model = DataTable
        exclude = ['index_delta']


class CityCriteriaTableSerializer(serializers.ModelSerializer):
    criteria = serializers.SerializerMethodField()
    index = serializers.SerializerMethodField()

    class Meta:
        model = AreaTableCriteria
        fields = ['criteria', 'index']

    def get_criteria(self, obj: AreaTableCriteria):
        return CriteriaSerializer(Criteria.objects.get(id=obj['criteria'])).data

    def get_index(self, obj):
        return float(str(obj['index'])[:5])


# Chart
class HomeSectorChartSerializer(serializers.ModelSerializer):
    sector = serializers.SerializerMethodField()
    bar = serializers.JSONField()
    index = serializers.FloatField()
    delta_index = serializers.FloatField()
    area_info = serializers.JSONField()

    class Meta:
        model = SectorTable
        fields = ['bar', 'sector', 'index', 'delta_index', 'area_info']

    def get_sector(self, obj):
        return SectorSerializer(Sector.objects.get(id=obj['sector'])).data


class SectorRegionBarChartSerializer(serializers.ModelSerializer):
    labels = serializers.ListField()
    datasets = serializers.JSONField()
    region = RegionSerializer()
    sector = SectorSerializer()
    file = UploadSerializer()

    class Meta:
        model = RegionSectorTable
        fields = '__all__'


class DataTableRowSerializer(serializers.Serializer):
    criteria_name = serializers.CharField()
    index = serializers.SerializerMethodField()

    def get_index(self, obj):
        return intspace(obj['index'], )


class PrimaryDataTableSerializer(serializers.ModelSerializer):
    data = serializers.ListSerializer(child=DataTableRowSerializer())

    class Meta:
        model = Area
        fields = "__all__"


class RegionDataTableSerializer(serializers.ModelSerializer):
    data = serializers.ListSerializer(child=DataTableRowSerializer())

    class Meta:
        model = Region
        fields = "__all__"
