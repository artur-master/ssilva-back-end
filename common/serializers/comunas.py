from common.models import Comuna
from rest_framework import serializers

# Serializador para el modelo Comuna


class ComunaSerializer(serializers.ModelSerializer):
    ProvinciaID = serializers.UUIDField(
        source='ProvinciaID.ProvinciaID'
    )

    class Meta:
        model = Comuna
        fields = ('Name', 'ComunaID', 'ProvinciaID')
