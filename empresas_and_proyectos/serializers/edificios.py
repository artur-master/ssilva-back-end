from empresas_and_proyectos.models.edificios import Edificio
from empresas_and_proyectos.models.inmuebles import Inmueble
from .inmuebles import CreateInmuebleSerializer, InmuebleSerializer
from rest_framework import serializers


class EdificioSerializer(serializers.ModelSerializer):
    Inmuebles = CreateInmuebleSerializer(many=True)

    class Meta:
        model = Edificio
        fields = ('Name', 'Inmuebles')


class ListEdificioSerializer(serializers.ModelSerializer):
    EdificioID = serializers.CharField(
        read_only=True
    )
    Name = serializers.CharField(
        read_only=True
    )
    Inmuebles = serializers.SerializerMethodField('get_inmuebles_edificio')

    class Meta:
        model = Edificio
        fields = ('EdificioID', 'Name', 'Inmuebles')

    def get_inmuebles_edificio(self, obj):
        inmuebles_edificio = Inmueble.objects.filter(EdificioID=obj)
        serializer = InmuebleSerializer(
            instance=inmuebles_edificio, context={'url': request}, many=True)
        return serializer.data
