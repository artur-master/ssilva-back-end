from ventas.models.empresas_compradoras import EmpresaCompradora
from common.validations import validate_rut_empresa_compradora
from rest_framework import serializers


class EmpresaCompradoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaCompradora
        fields = ('RazonSocial', 'Rut', 'Address')


class CreateEmpresaCompradoraSerializer(serializers.ModelSerializer):
    Rut = serializers.CharField(
        validators=[validate_rut_empresa_compradora],
        allow_null=True
    )

    class Meta:
        model = EmpresaCompradora
        fields = ('RazonSocial', 'Rut', 'Address')
