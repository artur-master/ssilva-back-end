from ventas.models.payment_forms import ProductoFinanciero
from rest_framework import serializers


class ProductoFinancieroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoFinanciero
        fields = ('Name', 'Value')
