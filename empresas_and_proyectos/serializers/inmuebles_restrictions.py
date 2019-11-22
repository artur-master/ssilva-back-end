from django.core.files.base import ContentFile
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from empresas_and_proyectos.models.inmuebles import Inmueble
from empresas_and_proyectos.models.inmuebles_restrictions import (
    InmuebleInmueble,
    InmuebleInmuebleType)
from empresas_and_proyectos.models.proyectos_logs import (
    ProyectoLog,
    ProyectoLogType)
from common import constants
from common.validations import revisar_restricciones
from common.services import return_current_user
from common.generate_pdf import render_create_restrictions_to_pdf
from rest_framework import serializers


class InmuebleInmuebleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InmuebleInmuebleType
        fields = ('InmuebleInmuebleTypeID', 'Name')


class InmuebleRestrictionSerializer(serializers.ModelSerializer):
    InmuebleBID = serializers.UUIDField(
        write_only=True
    )
    InmuebleInmuebleTypeID = serializers.UUIDField(
        write_only=True
    )
    InmuebleInmuebleType = serializers.CharField(
        source='InmuebleInmuebleTypeID.Name',
        read_only=True
    )
    InmuebleB = serializers.SerializerMethodField('get_inmueble_b')

    class Meta:
        model = InmuebleInmueble
        fields = ('InmuebleBID', 'InmuebleB',
                  'InmuebleInmuebleTypeID', 'InmuebleInmuebleType')

    def get_inmueble_b(self, obj):
        return "%s - %s" % (obj.InmuebleBID.InmuebleTypeID.Name,
                            obj.InmuebleBID.Number)

# Serializador para la busqueda de restricciones dado un uuid de un inmueble

class SearchInmuebleRestrictionSerializer(serializers.ModelSerializer):
    InmuebleAID = serializers.CharField(
        source='InmuebleAID.InmuebleID',
        read_only=True
    )
    InmuebleBID = serializers.CharField(
        source='InmuebleBID.InmuebleID',
        read_only=True
    )
    InmuebleInmuebleTypeID = serializers.CharField(
        source='InmuebleInmuebleTypeID.InmuebleInmuebleTypeID',
        read_only=True
    )
    InmuebleInmuebleType = serializers.CharField(
        source='InmuebleInmuebleTypeID.Name',
        read_only=True
    )
    InmuebleA = serializers.SerializerMethodField('get_inmueble_a')
    InmuebleB = serializers.SerializerMethodField('get_inmueble_b')

    class Meta:
        model = InmuebleInmueble
        fields = [
            'InmuebleAID',
            'InmuebleA',
            'InmuebleBID',
            'InmuebleB',
            'InmuebleInmuebleTypeID',
            'InmuebleInmuebleType']

    def get_inmueble_a(self, obj):
        return "%s - %s" % (obj.InmuebleAID.InmuebleTypeID.Name,
                            obj.InmuebleAID.Number)

    def get_inmueble_b(self, obj):
        return "%s - %s" % (obj.InmuebleBID.InmuebleTypeID.Name,
                            obj.InmuebleBID.Number)


class InmuebleInmuebleRestrictionSerializer(serializers.ModelSerializer):
    InmuebleAID = serializers.UUIDField(
        write_only=True
    )
    Restrictions = InmuebleRestrictionSerializer(
        many=True,
        required=False
    )
    InmuebleA = serializers.SerializerMethodField('get_inmueble_a')

    class Meta:
        model = InmuebleInmueble
        fields = ('InmuebleAID', 'InmuebleA', 'Restrictions')

    def create(self, validated_data):
        current_user = return_current_user(self)

        restrictions_data = validated_data.pop('Restrictions')

        # Inmueble "padre (A)" a crear restricciones
        inmueble = Inmueble.objects.get(
            InmuebleID=validated_data['InmuebleAID']
        )

        # Se identifica el proyecto al que pertenece el inmueble
        proyecto = inmueble.EtapaID.ProyectoID

        # Se buscan restricciones existentes en el sistema del inmueble "padre
        # (A)" a crear restricciones
        inmueble_restrictions = InmuebleInmueble.objects.filter(
            Q(InmuebleAID=inmueble) | Q(InmuebleBID=inmueble)
        )

        # Si existen restricciones se eliminan para crear las nuevas
        # restricciones
        if inmueble_restrictions.exists():
            inmueble_restrictions.delete()

        # Se revisa que los inmuebles "hijos (B)" no esten repetidos unos con
        # otros
        revisar_restricciones(restrictions_data)

        # Se crean las restricciones del inmueble "padre (A)" con los inmuebles
        # "hijos (B)"
        restrictions = []
        for restriction_data in restrictions_data:
            inmueble_inmueble_type = InmuebleInmuebleType.objects.get(
                InmuebleInmuebleTypeID=restriction_data['InmuebleInmuebleTypeID'])
            inmueble_b = Inmueble.objects.get(
                InmuebleID=restriction_data['InmuebleBID']
            )
            restriccion = InmuebleInmueble.objects.create(
                InmuebleAID=inmueble,
                InmuebleBID=inmueble_b,
                InmuebleInmuebleTypeID=inmueble_inmueble_type
            )
            restrictions.append(restriccion)

        # Creacion de foto de estado (pdf) actual de las restricciones

        # Se buscan las nuevas restricciones creadas para plasmarlas en el pdf
        inmueble_restrictions = InmuebleInmueble.objects.filter(
            Q(InmuebleAID=inmueble) | Q(InmuebleBID=inmueble)
        )

        context_dict = {
            'proyecto': proyecto,
            'inmueble_a': inmueble,
            'restricciones': inmueble_restrictions
        }

        pdf = render_create_restrictions_to_pdf(context_dict)

        pdf_generated = ContentFile(pdf)
        pdf_generated.name = "Documento.pdf"

        # Bitacora
        proyecto_log_type = ProyectoLogType.objects.get(
            Name=constants.PROYECTO_LOG_TYPE[3])

        comment = "Proyecto modificado, se crearon restricciones"

        ProyectoLog.objects.create(
            UserID=current_user,
            ProyectoID=proyecto,
            ProyectoLogTypeID=proyecto_log_type,
            Comment=comment,
            ProyectoDetailDocument=pdf_generated
        )

        return restrictions

    def update(self, instance, validated_data):
        inmueble_a = None
        for inmueble_restriction in instance:
            inmueble_a = inmueble_restriction.InmuebleAID.InmuebleID
        if not inmueble_a:
            raise ValidationError("InmueableAID not found")
        inmueble_a = Inmueble.objects.get(InmuebleID=inmueble_a)
        restrictions_data = validated_data.get('Restrictions')

        revisar_restricciones(restrictions_data)

        restrictions = []
        for restriction_data in restrictions_data:
            inmueble_inmueble_type = InmuebleInmuebleType.objects.get(
                InmuebleInmuebleTypeID=restriction_data['InmuebleInmuebleTypeID'])
            inmueble_b = Inmueble.objects.get(
                InmuebleID=restriction_data['InmuebleBID']
            )
            restriccion = InmuebleInmueble.objects.create(
                InmuebleAID=inmueble_a,
                InmuebleBID=inmueble_b,
                InmuebleInmuebleTypeID=inmueble_inmueble_type
            )
            restrictions.append(restriccion)
        return restrictions

    def get_inmueble_a(self, obj):
        return "%s - %s" % (obj.InmuebleAID.InmuebleTypeID.Name,
                            obj.InmuebleAID.Number)
