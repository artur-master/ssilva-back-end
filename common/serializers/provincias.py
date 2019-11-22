from common.models import Provincia
from rest_framework import serializers

# Serializador para modelo Provincia


class ProvinciaSerializer(serializers.ModelSerializer):
    RegionID = serializers.UUIDField(
        source='RegionID.RegionID'
    )

    class Meta:
        model = Provincia
        fields = ('Name', 'ProvinciaID', 'RegionID')
