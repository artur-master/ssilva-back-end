from common.models import ConstantNumeric
from rest_framework import serializers


# Serializador para el modelo ConstantNumeric

class ConstantNumericSerializer(serializers.ModelSerializer):
    Value = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = ConstantNumeric
        fields = ('Value',)   