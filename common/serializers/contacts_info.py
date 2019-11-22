from common.models import ContactInfoType
from rest_framework import serializers

# Serializador para el modelo ContactInfoType


class ContactInfoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfoType
        fields = ('ContactInfoTypeID', 'Name')


# Serializador para el modelo ContactInfo


class ContactInfoSerializer(serializers.ModelSerializer):
    ContactInfoTypeID = serializers.UUIDField(
        write_only=True
    )
    ContactInfoType = serializers.CharField(
        source='ContactInfoTypeID',
        read_only=True
    )    

    class Meta:
        model = ContactInfoType
        fields = ('ContactInfoTypeID', 'ContactInfoType', 'Name')