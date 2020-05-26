from ventas.models.empleadores import Empleador
from common.validations import validate_rut_empleador
from rest_framework import serializers


class EmpleadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleador
        fields = ('EmpleadorID', 'Rut', 'RazonSocial', 'Extra')


class CreateEmpleadorSerializer(serializers.ModelSerializer):
    Rut = serializers.CharField(
        write_only=True,
        allow_null=True,        
        required=False,
        allow_blank=True
    )

    class Meta:
        model = Empleador
        fields = ('Rut', 'RazonSocial', 'Extra')
