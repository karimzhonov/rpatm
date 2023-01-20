from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from ichd.api import serializers as ichd_serializers
from ichd import models as ichd_models
from ichd.utils import intspace

class AreaTableSerializer(serializers.ModelSerializer):
    area = ichd_serializers.AreaSerializer()
    criteria = serializers.SerializerMethodField()
    index = serializers.SerializerMethodField()
    delta_index = serializers.SerializerMethodField()

    class Meta:
        model = ichd_models.AreaTable
        fields = ['area', 'index', 'delta_index', 'criteria']

    def get_criteria(self, obj):
        for value in obj.criteria:
            value['index'] = intspace(value['index'])
        return obj.criteria

    @extend_schema_field(serializers.FloatField())
    def get_index(self, obj: ichd_models.AreaTable):
        return obj.areatablecriteria_set.filter(criteria__main=True).order_by('criteria__order').first().index

    @extend_schema_field(serializers.FloatField())
    def get_delta_index(self, obj: ichd_models.AreaTable):
        delta_index = obj.areatablecriteria_set.filter(criteria__main=True).order_by('criteria__order').first().delta
        return str(delta_index) if delta_index <= 0 else f'+{delta_index}'
