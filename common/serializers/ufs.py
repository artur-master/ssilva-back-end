from common.models import UF
from rest_framework import serializers

# Serializador para modelo UF


class UFSerializer(serializers.ModelSerializer):
    Value = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = UF
        fields = ('Date', 'Value')