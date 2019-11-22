from common.models import Region
from rest_framework import serializers

# Serializador para modelo Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('Name', 'RegionID')
