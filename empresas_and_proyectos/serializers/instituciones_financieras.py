from empresas_and_proyectos.models.instituciones_financieras import InstitucionFinanciera
from rest_framework import serializers


class InstitucionFinancieraSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitucionFinanciera
        fields = ('InstitucionFinancieraID', 'Name')
