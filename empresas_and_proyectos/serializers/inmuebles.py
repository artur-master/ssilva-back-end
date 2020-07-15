from empresas_and_proyectos.models.inmuebles import (
    InmuebleType,
    Orientation,
    Tipologia,
    Inmueble,
    InmuebleState)
from rest_framework import serializers
from common.services import get_full_path_x


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
    MaximumDiscount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )
    Up_Print = serializers.SerializerMethodField(
        'get_blueprint_url')

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
            'MaximumDiscount',
            'CotizacionDuration',
            'InmuebleStateID',
            'BluePrint',
            'Up_Print',
            'InmuebleState')
    
    def get_blueprint_url(self, obj):
        if obj.Up_Print and hasattr(
                obj.Up_Print, 'url'):
            url = self.context['url']
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.Up_Print.url)
        else:
            return ""

    def update(self, instance, validated_data):
        if 'Floor' in validated_data:
            instance.Floor = validated_data.get('Floor')
        if 'BathroomQuantity' in validated_data:
            instance.BathroomQuantity = validated_data.get('BathroomQuantity')
        if 'BedroomsQuantity' in validated_data:
            instance.BedroomsQuantity = validated_data.get('BedroomsQuantity')
        if 'UtilSquareMeters' in validated_data:
            instance.UtilSquareMeters = validated_data.get('UtilSquareMeters')
        if 'TerraceSquareMeters' in validated_data:
            instance.TerraceSquareMeters = validated_data.get('TerraceSquareMeters')
        if 'LodgeSquareMeters' in validated_data:
            instance.LodgeSquareMeters = validated_data.get('LodgeSquareMeters')
        if 'TotalSquareMeters' in validated_data:
            instance.TotalSquareMeters = validated_data.get('TotalSquareMeters')
        if 'IsNotUsoyGoce' in validated_data:
            instance.IsNotUsoyGoce = validated_data.get('IsNotUsoyGoce')
        if 'Price' in validated_data:
            instance.Price = validated_data.get('Price')
        if 'MaximumDiscount' in validated_data:
            instance.MaximumDiscount = validated_data.get('MaximumDiscount')

        instance.save()

        return instance
        
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
    MaximumDiscount = serializers.DecimalField(
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
            'MaximumDiscount',
            'CotizacionDuration',
            'InmuebleStateID',
            'InmuebleState')
