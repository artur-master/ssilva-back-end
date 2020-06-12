from ventas.models.payment_forms import Cuota
from rest_framework import serializers


class ListCuotaSerializer(serializers.ModelSerializer):
    Amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    Date = serializers.DateTimeField(
        read_only=True
    )
    Observacion = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Cuota
        fields = ('Amount', 'Date', 'Observacion')


class CreateCuotaSerializer(serializers.ModelSerializer):
    Amount = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
    )
    Date = serializers.DateTimeField(
        write_only=True
    )
    Observacion = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    class Meta:
        model = Cuota
        fields = ('Amount', 'Date', 'Observacion')
