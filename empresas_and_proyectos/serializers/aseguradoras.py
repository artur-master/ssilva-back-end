from empresas_and_proyectos.models.aseguradoras import Aseguradora
from rest_framework import serializers


class AseguradoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aseguradora
        fields = ('AseguradoraID', 'Name')
