# coding: utf-8
from rest_framework import serializers

from ventas.models.payment_forms import PayType


class PayTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayType
        fields = ('PayTypeID', 'Name')
