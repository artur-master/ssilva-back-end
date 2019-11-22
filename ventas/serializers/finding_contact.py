from ventas.models.finding_contact import (
    FindingType,
    ContactMethodType)
from rest_framework import serializers


class FindingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindingType
        fields = ('FindingTypeID', 'Name')


class ContactMethodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMethodType
        fields = ('ContactMethodTypeID', 'Name')
