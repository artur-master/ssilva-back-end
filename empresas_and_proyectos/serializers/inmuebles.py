from empresas_and_proyectos.models.inmuebles import (
    InmuebleType,
    Orientation,
    Tipologia,
    Inmueble,
    InmuebleState)
from rest_framework import serializers


class ListOrientationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orientation
        fields = ('OrientationID', 'Name', 'Description')


class OrientationSerializer(serializers.ModelSerializer):
    Name = serializers.CharField(
        read_only=True
    )
    OrientationID = serializers.UUIDField(
        write_only=True
    )

    class Meta:
        model = Orientation
        fields = ('OrientationID', 'Name', 'Description')


class TipologiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipologia
        fields = ('TipologiaID', 'Name', 'Description')


class InmuebleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InmuebleType
        fields = ('InmuebleTypeID', 'Name', 'Description')


class InmuebleStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InmuebleState
        fields = ('InmuebleStateID', 'Name')


class InmuebleSerializer(serializers.ModelSerializer):
    InmuebleID = serializers.CharField(
        read_only=True
    )
    InmuebleTypeID = serializers.CharField(
        source='InmuebleTypeID.InmuebleTypeID',
        read_only=True
    )
    InmuebleType = serializers.CharField(
        source='InmuebleTypeID.Name',
        read_only=True
    )
    TipologiaID = serializers.CharField(
        source='TipologiaID.TipologiaID',
        read_only=True,
        allow_null=True
    )
    Tipologia = serializers.CharField(
        source='TipologiaID.Description',
        read_only=True
    )
    Orientation = ListOrientationSerializer(
        source='OrientationID',
        many=True
    )
    InmuebleStateID = serializers.CharField(
        source='InmuebleStateID.InmuebleStateID',
        read_only=True
    )
    InmuebleState = serializers.CharField(
        source='InmuebleStateID.Name',
        read_only=True
    )
    Floor = serializers.IntegerField(
        allow_null=True
    )
    BathroomQuantity = serializers.IntegerField(
        allow_null=True
    )
    BedroomsQuantity = serializers.IntegerField(
        allow_null=True
    )
    UtilSquareMeters = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        allow_null=True
    )
    TerraceSquareMeters = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        allow_null=True
    )
    LodgeSquareMeters = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        allow_null=True
    )
    TotalSquareMeters = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        allow_null=True
    )
    Price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )
    MaximunDiscount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = Inmueble
        fields = (
            'InmuebleID',
            'InmuebleTypeID',
            'InmuebleType',
            'TipologiaID',
            'Tipologia',
            'Orientation',
            'Number',
            'Floor',
            'BathroomQuantity',
            'BedroomsQuantity',
            'UtilSquareMeters',
            'TerraceSquareMeters',
            'LodgeSquareMeters',
            'TotalSquareMeters',
            'IsNotUsoyGoce',
            'Price',
            'MaximunDiscount',
            'CotizacionDuration',
            'InmuebleStateID',
            'BluePrint',
            'Up_Print',
            'InmuebleState')


class CreateInmuebleSerializer(serializers.ModelSerializer):
    InmuebleID = serializers.UUIDField(
        write_only=True,
        allow_null=True,
        required=False
    )
    InmuebleTypeID = serializers.CharField(
        write_only=True
    )
    InmuebleType = serializers.CharField(
        source='InmuebleTypeID.Name',
        read_only=True
    )
    TipologiaID = serializers.CharField(
        write_only=True,
        allow_null=True
    )
    Tipologia = serializers.CharField(
        source='TipologiaID.Name',
        read_only=True
    )
    Orientation = OrientationSerializer(
        source='OrientationID',
        many=True,
        allow_null=True
    )
    InmuebleStateID = serializers.CharField(
        write_only=True
    )
    InmuebleState = serializers.CharField(
        source='InmuebleStateID.Name',
        read_only=True
    )
    Floor = serializers.IntegerField(
        allow_null=True
    )
    BathroomQuantity = serializers.IntegerField(
        allow_null=True
    )
    BedroomsQuantity = serializers.IntegerField(
        allow_null=True
    )
    UtilSquareMeters = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        allow_null=True
    )
    TerraceSquareMeters = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        allow_null=True
    )
    LodgeSquareMeters = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        allow_null=True
    )
    TotalSquareMeters = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        allow_null=True
    )
    Price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )
    MaximunDiscount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        allow_null=True
    )
    CotizacionDuration = serializers.IntegerField(
        allow_null=True
    )

    class Meta:
        model = Inmueble
        fields = (
            'InmuebleID',
            'InmuebleTypeID',
            'InmuebleType',
            'TipologiaID',
            'Tipologia',
            'Orientation',
            'Number',
            'Floor',
            'BathroomQuantity',
            'BedroomsQuantity',
            'UtilSquareMeters',
            'TerraceSquareMeters',
            'LodgeSquareMeters',
            'TotalSquareMeters',
            'IsNotUsoyGoce',
            'Price',
            'MaximunDiscount',
            'CotizacionDuration',
            'InmuebleStateID',
            'InmuebleState')
