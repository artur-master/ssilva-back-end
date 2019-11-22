from rest_framework import serializers
from ventas.models.patrimonies import Patrimony


class PatrimonySerializer(serializers.ModelSerializer):
    RealState = serializers.IntegerField(
        required=False
    )
    Vehicle = serializers.IntegerField(
        required=False
    )
    DownPayment = serializers.IntegerField(
        required=False
    )
    Other = serializers.IntegerField(
        required=False
    )
    CreditCard = serializers.JSONField(required=False)
    CreditoConsumo = serializers.JSONField(required=False)
    CreditoHipotecario = serializers.JSONField(required=False)
    PrestamoEmpleador = serializers.JSONField(required=False)
    CreditoComercio = serializers.JSONField(required=False)
    DeudaIndirecta = serializers.JSONField(required=False)
    AnotherCredit = serializers.JSONField(required=False)
    Deposits = serializers.FloatField(required=False)
    Rent = serializers.FloatField(required=False)

    class Meta:
        model = Patrimony
        fields = ('RealState', 'Vehicle', 'DownPayment',
                  'Other', 'CreditCard', 'CreditoConsumo',
                  'CreditoHipotecario', 'PrestamoEmpleador', 'CreditoComercio',
                  'DeudaIndirecta', 'AnotherCredit', 'Deposits', 'Rent')
