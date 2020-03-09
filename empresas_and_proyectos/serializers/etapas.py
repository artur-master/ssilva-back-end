import uuid

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from common import constants
from empresas_and_proyectos.models.edificios import Edificio
from empresas_and_proyectos.models.etapas import (
    Etapa,
    EtapaState)
from empresas_and_proyectos.models.proyectos import (
    Proyecto,
    UserProyecto,
    UserProyectoType,
    ProyectoApprovalState)
from empresas_and_proyectos.models.proyectos_logs import (
    ProyectoLog,
    ProyectoLogType)
from empresas_and_proyectos.models.inmuebles import (
    InmuebleType,
    Tipologia,
    Inmueble,
    InmuebleState,
    Orientation)
from history.models import (
    CounterHistory,
    HistoricalProyecto,
    HistoricalEtapa,
    HistoricalEdificio,
    HistoricalInmueble)
from common.services import (
    return_current_user,
    get_or_none,
    import_excel_inmuebles,
    is_nan)
from common.validations import (
    CustomValidation,
    revisar_numeros_duplicados,
    revisar_numeros_duplicados_excel)
from common.notifications import (
    crear_notificacion_etapa_sin_fecha_de_ventas,
    eliminar_notificacion_proyecto_sin_inmuebles)
from users.models import User, Permission
from .edificios import (
    EdificioSerializer,
    ListEdificioSerializer)
from .inmuebles import (CreateInmuebleSerializer, InmuebleSerializer)
from common.generate_pdf import render_create_etapa_to_pdf
from rest_framework import serializers, status
from django_bulk_update.helper import bulk_update

from empresas_and_proyectos.snippets.inmuebles import insert_properties_orientaations


class EtapaStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtapaState
        fields = ('EtapaStateID', 'Name')


class ListEtapaSerializer(serializers.ModelSerializer):
    EtapaID = serializers.CharField(
        read_only=True,
        allow_null=True
    )
    Name = serializers.CharField(
        read_only=True,
        allow_null=True
    )

    EtapaStateID = serializers.CharField(
        source='EtapaStateID.EtapaStateID',
        allow_null=True
    )
    EtapaState = EtapaStateSerializer(source='EtapaStateID', read_only=True, allow_null=True)
    Edificios = serializers.SerializerMethodField('get_edificios_etapa', allow_null=True)
    Inmuebles = serializers.SerializerMethodField('get_inmuebles_etapa', allow_null=True)

    SalesStartDate = serializers.DateTimeField(
        allow_null=True
    )

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('etapa_edificio')
        return queryset

    class Meta:
        model = Etapa
        fields = ('EtapaID', 'Name', 'SalesStartDate',
                  'EtapaState', 'EtapaStateID', 'Edificios', 'Inmuebles')

    def get_edificios_etapa(self, obj):
        edificios_etapa = Edificio.objects.filter(EtapaID=obj)
        serializer = ListEdificioSerializer(
            instance=edificios_etapa, many=True)
        return serializer.data

    def get_inmuebles_etapa(self, obj):
        inmuebles_etapa = Inmueble.objects.filter(EtapaID=obj, EdificioID=None)
        serializer = InmuebleSerializer(
            instance=inmuebles_etapa, many=True)
        return serializer.data


class BeginVentaSerializer(serializers.ModelSerializer):
    SalesStartDate = serializers.DateTimeField(
        write_only=True
    )

    class Meta:
        model = Etapa
        fields = ('SalesStartDate',)

    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        sales_start_date = validated_data['SalesStartDate']

        if instance.SalesStartDate:
            raise CustomValidation(
                "Fecha de inicio de ventas ya ha sido ingresada",
                status_code=status.HTTP_409_CONFLICT)

        if not sales_start_date:
            raise CustomValidation(
                "Debe ingresar fecha de inicio de ventas",
                status_code=status.HTTP_409_CONFLICT)

        instance.SalesStartDate = sales_start_date
        instance.save()

        # Registro en bitacora de proyecto
        proyecto_log_type = ProyectoLogType.objects.get(
            Name=constants.PROYECTO_LOG_TYPE[11])

        ProyectoLog.objects.create(
            UserID=current_user,
            ProyectoID=instance.ProyectoID,
            ProyectoLogTypeID=proyecto_log_type
        )

        return instance


# Serializadores de Etapas, A Futuro ordenar bien estos serializadores ya que hay serializadores
# de mas que se fueron creando debido a cambios que iban apareciendo cuando ya estaban funcionando los demas


class CreateEtapaSingleSerializer(serializers.ModelSerializer):
    ProyectoID = serializers.UUIDField(allow_null=True)
    SalesStartDate = serializers.DateTimeField(allow_null=True)
    EtapaStateID = serializers.UUIDField(allow_null=True)
    EtapaState = EtapaStateSerializer(source='EtapaStateID', allow_null=True, read_only=True)

    class Meta:
        model = Etapa
        fields = ('ProyectoID',
                  'Name',
                  'SalesStartDate',
                  'EtapaStateID',
                  'EtapaState')

    def create(self, validated_data):
        proyecto_id = validated_data['ProyectoID']
        sales_start_date = validated_data['SalesStartDate']
        etapa_state_id = validated_data['EtapaStateID']

        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        etapa_state = EtapaState.objects.get(EtapaStateID=etapa_state_id)

        if not sales_start_date:
            sales_start_date = None

        instance = Etapa.objects.create(
            Name=validated_data['Name'],
            SalesStartDate=sales_start_date,
            ProyectoID=proyecto,
            EtapaStateID=etapa_state
        )

        if not sales_start_date:
            user_proyecto_type = UserProyectoType.objects.get(
                Name=constants.USER_PROYECTO_TYPE[1])

            jefe_proyecto = UserProyecto.objects.filter(
                ProyectoID=proyecto, UserProyectoTypeID=user_proyecto_type)

            # Permiso Monitorea Proyectos
            permission = Permission.objects.get(Name=constants.PERMISSIONS[14])

            usuarios_monitorea_proyectos = User.objects.filter(
                RoleID__PermissionID=permission)

            crear_notificacion_etapa_sin_fecha_de_ventas(
                instance, self.current_user, jefe_proyecto, usuarios_monitorea_proyectos)

        return instance

# Serializador para actualizar etapas


class EtapaSerializer(serializers.ModelSerializer):
    EtapaID = serializers.UUIDField(
        write_only=True
    )
    Edificios = EdificioSerializer(
        many=True,
        required=False
    )
    Inmuebles = CreateInmuebleSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Etapa
        fields = ('EtapaID', 'Edificios', 'Inmuebles')

    def create(self, validated_data):
        inmuebles_orientation = dict()
        current_user = return_current_user(self)
        etapa_id = validated_data['EtapaID']
        edificios_data = validated_data.pop('Edificios')
        inmuebles_sin_edificio_data = validated_data.pop('Inmuebles')

        instance = Etapa.objects.get(EtapaID=etapa_id)

        # Arreglos de ayuda para guardar los inmuebles antes y despues de
        # modificarlos
        inmuebles_not_changed = []
        edificio_inmueble_not_changed = []
        inmuebles_sin_edificio_not_changed = []
        inmuebles_changed = []
        inmuebles_sin_edificio_changed = []

        proyecto = instance.ProyectoID

        # proyecto historico para historial de etapa
        counter = CounterHistory.objects.get(ProyectoID=proyecto)

        proyecto_hist = HistoricalProyecto.objects.create(
            ProyectoID=proyecto.ProyectoID,
            Counter=counter.Count,
            Name=proyecto.Name,
            Symbol=proyecto.Symbol,
            Address=proyecto.Address,
            InstitucionFinancieraID=proyecto.InstitucionFinancieraID,
            ComunaID=proyecto.ComunaID,
            InmobiliariaID=proyecto.InmobiliariaID,
            ConstructoraID=proyecto.ConstructoraID,
            CotizacionDuration=proyecto.CotizacionDuration,
            GuaranteeAmount=proyecto.GuaranteeAmount,
            PlanMediosState=proyecto.PlanMediosState,
            BorradorPromesaState=proyecto.BorradorPromesaState,
            IngresoComisionesState=proyecto.IngresoComisionesState
        )

        # creacion de historial para etapa
        etapa_hist = HistoricalEtapa.objects.create(
            Name=instance.Name,
            SalesStartDate=instance.SalesStartDate,
            EtapaStateID=instance.EtapaStateID,
            ProyectoID=proyecto_hist
        )

        inmuebles_etapa = Inmueble.objects.filter(EtapaID=instance)

        inmuebles_sin_edificio = Inmueble.objects.filter(
            EtapaID=instance, EdificioID=None)

        edificios_etapa = Edificio.objects.filter(EtapaID=instance)

        for inmueble in inmuebles_sin_edificio:
            inmuebles_sin_edificio_not_changed.append(inmueble)

        for inmueble in inmuebles_etapa:
            inmuebles_not_changed.append(inmueble)
            edificio_inmueble_not_changed.append(inmueble.EdificioID)

        for inmueble_edificio in inmuebles_not_changed:
            if not inmueble_edificio.EdificioID:
                inmuebles_not_changed.remove(inmueble_edificio)

        if edificios_etapa.exists():
            edificios_etapa.delete()

        if inmuebles_etapa.exists():
            inmuebles_etapa.delete()

        for edificio_data in edificios_data:
            inmuebles_data = edificio_data.pop('Inmuebles')
            edificio = Edificio.objects.create(
                Name=edificio_data['Name'],
                EtapaID=instance
            )

            # creacion de historial para edificio
            edificio_hist = HistoricalEdificio.objects.create(
                Name=edificio_data['Name'],
                EtapaID=etapa_hist
            )

            revisar_numeros_duplicados(inmuebles_data, edificio)

            inmuebles_creados = list()
            historicos = list()
            orientations_uuid = list()
            historicos_orientation = dict()
            orientations_historicos_uuid = list()

            for inmueble_data in inmuebles_data:
                inmueble_id = inmueble_data['InmuebleID']
                inmueble_type = InmuebleType.objects.get(
                    InmuebleTypeID=inmueble_data['InmuebleTypeID'])
                tipologia_id = inmueble_data['TipologiaID']
                maximun_discount = inmueble_data['MaximunDiscount']

                tipologia = get_or_none(Tipologia, TipologiaID=tipologia_id)

                if not maximun_discount:
                    maximun_discount = None

                if inmueble_type.Name == constants.INMUEBLE_TYPE[0] and not tipologia_id:
                    raise CustomValidation(
                        "Los departamentos deben tener tipología",
                        status_code=status.HTTP_409_CONFLICT)

                inmueble_state = InmuebleState.objects.get(
                    InmuebleStateID=inmueble_data['InmuebleStateID'])

                inmueble_creado = Inmueble()
                inmueble_creado.InmuebleTypeID = inmueble_type
                inmueble_creado.TipologiaID = tipologia
                inmueble_creado.EtapaID = instance
                inmueble_creado.EdificioID = edificio
                inmueble_creado.InmuebleStateID = inmueble_state
                inmueble_creado.Number = inmueble_data['Number']
                inmueble_creado.Floor = inmueble_data['Floor']
                inmueble_creado.BathroomQuantity = inmueble_data['BathroomQuantity']
                inmueble_creado.BedroomsQuantity = inmueble_data['BedroomsQuantity']
                inmueble_creado.UtilSquareMeters = inmueble_data['UtilSquareMeters']
                inmueble_creado.TerraceSquareMeters = inmueble_data['TerraceSquareMeters']
                inmueble_creado.LodgeSquareMeters = inmueble_data['LodgeSquareMeters']
                inmueble_creado.TotalSquareMeters = 0
                inmueble_creado.IsNotUsoyGoce = inmueble_data['IsNotUsoyGoce']
                inmueble_creado.Price = inmueble_data['Price']
                inmueble_creado.MaximunDiscount = maximun_discount
                inmueble_creado.CotizacionDuration = proyecto.CotizacionDuration

                if inmueble_id:
                    inmueble_creado.InmuebleID = inmueble_id

                for orientation_data in inmueble_data['OrientationID']:
                    orientations_uuid.append(orientation_data['OrientationID'])

                inmuebles_orientation[inmueble_creado.InmuebleID] = orientations_uuid

                inmuebles_creados.append(inmueble_creado)

                # Creacion de historial para inmuebles con edificio
                inmueble_hist = HistoricalInmueble()
                inmueble_hist.InmuebleTypeID = inmueble_type
                inmueble_hist.TipologiaID = tipologia
                inmueble_hist.EtapaID = etapa_hist
                inmueble_hist.EdificioID = edificio_hist
                inmueble_hist.InmuebleStateID = inmueble_state
                inmueble_hist.Number = inmueble_data['Number']
                inmueble_hist.Floor = inmueble_data['Floor']
                inmueble_hist.BathroomQuantity = inmueble_data['BathroomQuantity']
                inmueble_hist.BedroomsQuantity = inmueble_data['BedroomsQuantity']
                inmueble_hist.UtilSquareMeters = inmueble_data['UtilSquareMeters']
                inmueble_hist.TerraceSquareMeters = inmueble_data['TerraceSquareMeters']
                inmueble_hist.LodgeSquareMeters = inmueble_data['LodgeSquareMeters']
                inmueble_hist.TotalSquareMeters = 0
                inmueble_hist.IsNotUsoyGoce = inmueble_data['IsNotUsoyGoce']
                inmueble_hist.Price = inmueble_data['Price']
                inmueble_hist.MaximunDiscount = maximun_discount
                inmueble_hist.CotizacionDuration = proyecto.CotizacionDuration

                if inmueble_id:
                    inmueble_hist.InmuebleID = inmueble_id

                for orientation_data in inmueble_data['OrientationID']:
                    orientations_historicos_uuid.append(orientation_data['OrientationID'])

                historicos_orientation[inmueble_hist.InmuebleID] = orientations_historicos_uuid

                historicos.append(inmueble_hist)

            Inmueble.objects.bulk_create(inmuebles_creados)
            HistoricalInmueble.objects.bulk_create(historicos)

        revisar_numeros_duplicados(inmuebles_sin_edificio_data, None)

        creados_inmuebles = list()
        historicos_inmuebles = list()
        inmuebles_orientation_sin_edificio = dict()
        orientations_uuid_sin_edificio = list()

        for inmueble_data in inmuebles_sin_edificio_data:
            inmueble_id = inmueble_data['InmuebleID']

            inmueble_type = InmuebleType.objects.get(
                InmuebleTypeID=inmueble_data['InmuebleTypeID'])

            tipologia_id = inmueble_data['TipologiaID']

            tipologia = get_or_none(Tipologia, TipologiaID=tipologia_id)
            maximun_discount = inmueble_data['MaximunDiscount']

            if inmueble_type.Name == constants.INMUEBLE_TYPE[0] and not tipologia_id:
                raise CustomValidation(
                    "Los departamentos deben tener tipología",
                    status_code=status.HTTP_409_CONFLICT)

            inmueble_state = InmuebleState.objects.get(
                InmuebleStateID=inmueble_data['InmuebleStateID'])

            inmueble_creado = Inmueble()
            inmueble_creado.InmuebleTypeID = inmueble_type
            inmueble_creado.TipologiaID = tipologia
            inmueble_creado.EtapaID = instance
            inmueble_creado.EdificioID = None
            inmueble_creado.InmuebleStateID = inmueble_state
            inmueble_creado.Number = inmueble_data['Number']
            inmueble_creado.Floor = inmueble_data['Floor']
            inmueble_creado.BathroomQuantity = inmueble_data['BathroomQuantity']
            inmueble_creado.BedroomsQuantity = inmueble_data['BedroomsQuantity']
            inmueble_creado.UtilSquareMeters = inmueble_data['UtilSquareMeters']
            inmueble_creado.TerraceSquareMeters = inmueble_data['TerraceSquareMeters']
            inmueble_creado.LodgeSquareMeters = inmueble_data['LodgeSquareMeters']
            inmueble_creado.TotalSquareMeters = 0
            inmueble_creado.IsNotUsoyGoce = inmueble_data['IsNotUsoyGoce']
            inmueble_creado.Price = inmueble_data['Price']
            inmueble_creado.MaximunDiscount = maximun_discount
            inmueble_creado.CotizacionDuration = proyecto.CotizacionDuration

            if inmueble_id:
                inmueble_creado.InmuebleID = inmueble_id

            for orientation_data in inmueble_data['OrientationID']:
                orientations_uuid_sin_edificio.append(orientation_data['OrientationID'])

            inmuebles_orientation_sin_edificio[inmueble_creado.InmuebleID] = orientations_uuid_sin_edificio

            creados_inmuebles.append(inmueble_creado)

            # Creacion de historial para inmuebles sin edificio
            inmueble_hist = HistoricalInmueble()
            inmueble_hist.InmuebleTypeID = inmueble_type
            inmueble_hist.TipologiaID = tipologia
            inmueble_hist.EtapaID = etapa_hist
            inmueble_hist.EdificioID = None
            inmueble_hist.InmuebleStateID = inmueble_state
            inmueble_hist.Number = inmueble_data['Number']
            inmueble_hist.Floor = inmueble_data['Floor']
            inmueble_hist.BathroomQuantity = inmueble_data['BathroomQuantity']
            inmueble_hist.BedroomsQuantity = inmueble_data['BedroomsQuantity']
            inmueble_hist.UtilSquareMeters = inmueble_data['UtilSquareMeters']
            inmueble_hist.TerraceSquareMeters = inmueble_data['TerraceSquareMeters']
            inmueble_hist.LodgeSquareMeters = inmueble_data['LodgeSquareMeters']
            inmueble_hist.TotalSquareMeters = 0
            inmueble_hist.IsNotUsoyGoce = inmueble_data['IsNotUsoyGoce']
            inmueble_hist.Price = inmueble_data['Price']
            inmueble_hist.MaximunDiscount = maximun_discount
            inmueble_hist.CotizacionDuration = proyecto.CotizacionDuration

            if inmueble_id:
                inmueble_hist.InmuebleID = inmueble_id

            historicos_inmuebles.append(inmueble_hist)

        Inmueble.objects.bulk_create(creados_inmuebles)
        HistoricalInmueble.objects.bulk_create(historicos_inmuebles)

        # Agregar orientaciones a inmuebles con edificios
        uuids_list = [key for key in inmuebles_orientation]

        inmuebles_orientations = Inmueble.objects.filter(InmuebleID__in=uuids_list)
        inms = list()
        for i in inmuebles_orientation:
            inmueble_ori = get_object_or_404(inmuebles_orientations, InmuebleID=i)
            for orientation_id in inmuebles_orientation[i]:
                orientation = get_object_or_404(Orientation, OrientationID=orientation_id)
                inmueble_ori.OrientationID.add(orientation)
            inms.append(inmueble_ori)

        bulk_update(inms)

        # Agregar orientaciones a inmuebles sin edificios
        uuids_list = [key for key in inmuebles_orientation_sin_edificio]

        inmuebles_orientations = Inmueble.objects.filter(InmuebleID__in=uuids_list)
        inms = list()
        for i in inmuebles_orientation_sin_edificio:
            inmueble_ori = get_object_or_404(inmuebles_orientations, InmuebleID=i)
            for orientation_id in inmuebles_orientation_sin_edificio[i]:
                orientation = get_object_or_404(Orientation, OrientationID=orientation_id)
                inmueble_ori.OrientationID.add(orientation)
            inms.append(inmueble_ori)

        bulk_update(inms)

        # PDF de Bitacora esta comentada debido a que ralentizaba demasiado la respuesta del endpoint
        # Se debe optimizar esto para poder crear el pdf de bitacora


        # inmuebles = Inmueble.objects.filter(EtapaID=instance)
        # inmuebles_sin_edificios = Inmueble.objects.filter(
        #     EtapaID=instance, EdificioID=None)
        #
        # for inmueble in inmuebles:
        #     if inmueble.EdificioID:
        #         inmuebles_changed.append(inmueble)
        #
        # for inmueble in inmuebles_sin_edificios:
        #     if not inmueble.EdificioID:
        #         inmuebles_sin_edificio_changed.append(inmueble)

        # # Bitacora
        # context_dict = {
        #     'etapa': instance,
        #     'datos_modificados': validated_data,
        #     'estado_etapa': instance.EtapaStateID,
        #     'inmuebles': inmuebles_not_changed,
        #     'inmuebles_nuevos': inmuebles_changed,
        #     'inmuebles_sin_edificios': inmuebles_sin_edificio_not_changed,
        #     'inmuebles_sin_edificios_nuevos': inmuebles_sin_edificio_changed,
        #     'edificios': edificio_inmueble_not_changed
        # }
        #
        # pdf = render_update_etapa_to_pdf(context_dict)
        #
        # pdf_generated = ContentFile(pdf)
        # pdf_generated.name = "Documento.pdf"

        proyecto_log_type = ProyectoLogType.objects.get(
            Name=constants.PROYECTO_LOG_TYPE[2])

        comment = "Proyecto modificado, se modifico %s" % (instance.Name)

        ProyectoLog.objects.create(
            UserID=current_user,
            ProyectoID=proyecto,
            ProyectoLogTypeID=proyecto_log_type,
            Comment=comment,
            Counter=counter.Count
            # ProyectoDetailDocument=pdf_generated
        )

        counter.Count += 1
        counter.save()

        # Cambio estado de aprobacion del proyecto
        proyecto_approval_state = ProyectoApprovalState.objects.get(
            Name=constants.PROYECTO_APPROVAL_STATE[1])

        proyecto.ProyectoApprovalState = proyecto_approval_state
        proyecto.save()

        return instance


class CreateEtapaSerializer(serializers.ModelSerializer):
    EtapaID = serializers.UUIDField(
        write_only=True
    )
    EtapaStateID = serializers.UUIDField(
        write_only=True
    )
    Edificios = EdificioSerializer(
        many=True,
        required=False
    )
    Inmuebles = CreateInmuebleSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Etapa
        fields = ('EtapaID', 'EtapaStateID',
                  'Edificios', 'Inmuebles')

    def create(self, validated_data):
        inmuebles_orientation = dict()
        current_user = return_current_user(self)

        edificios_data = validated_data.pop('Edificios')
        inmuebles_sin_edificio_data = validated_data.pop('Inmuebles')
        etapa_state_id = validated_data.pop('EtapaStateID')

        etapa_state = EtapaState.objects.get(EtapaStateID=etapa_state_id)

        instance = Etapa.objects.get(
            EtapaID=validated_data['EtapaID']
        )

        proyecto = instance.ProyectoID

        # proyecto historico para historial de etapa
        counter = CounterHistory.objects.get(ProyectoID=proyecto)

        proyecto_hist = HistoricalProyecto.objects.create(
            ProyectoID=proyecto.ProyectoID,
            Counter=counter.Count,
            Name=proyecto.Name,
            Symbol=proyecto.Symbol,
            Address=proyecto.Address,
            InstitucionFinancieraID=proyecto.InstitucionFinancieraID,
            ComunaID=proyecto.ComunaID,
            InmobiliariaID=proyecto.InmobiliariaID,
            ConstructoraID=proyecto.ConstructoraID,
            CotizacionDuration=proyecto.CotizacionDuration,
            GuaranteeAmount=proyecto.GuaranteeAmount,
            PlanMediosState=proyecto.PlanMediosState,
            BorradorPromesaState=proyecto.BorradorPromesaState,
            IngresoComisionesState=proyecto.IngresoComisionesState
        )

        sales_start_date = instance.SalesStartDate

        if not sales_start_date:
            sales_start_date = None

        # creacion de historial para etapa
        etapa_hist = HistoricalEtapa.objects.create(
            Name=instance.Name,
            SalesStartDate=sales_start_date,
            EtapaStateID=etapa_state,
            ProyectoID=proyecto_hist
        )

        for edificio_data in edificios_data:
            inmuebles_data = edificio_data.pop('Inmuebles')

            edificio = get_or_none(
                Edificio,
                Name=edificio_data['Name'],
                EtapaID=instance)
            if not edificio:
                edificio = Edificio.objects.create(
                    Name=edificio_data['Name'],
                    EtapaID=instance
                )

            # creacion de historial para edificio
            edificio_hist = HistoricalEdificio.objects.create(
                Name=edificio_data['Name'],
                EtapaID=etapa_hist
            )

            revisar_numeros_duplicados(inmuebles_data, edificio)

            inmuebles_creados = list()
            historicos = list()
            orientations_uuid = list()
            historicos_orientation = dict()
            orientations_historicos_uuid = list()

            for inmueble_data in inmuebles_data:
                inmueble_type = InmuebleType.objects.get(
                    InmuebleTypeID=inmueble_data['InmuebleTypeID'])
                tipologia_id = inmueble_data['TipologiaID']
                maximun_discount = inmueble_data['MaximunDiscount']

                if tipologia_id:
                    tipologia = Tipologia.objects.get(
                        TipologiaID=tipologia_id)
                else:
                    tipologia = None

                if not maximun_discount:
                    maximun_discount = None

                if inmueble_type.Name == constants.INMUEBLE_TYPE[0] and not tipologia_id:
                    raise CustomValidation(
                        "Los departamentos deben tener tipología",
                        status_code=status.HTTP_409_CONFLICT)

                inmueble_state = InmuebleState.objects.get(
                    InmuebleStateID=inmueble_data['InmuebleStateID'])

                inmueble_creado = Inmueble()
                inmueble_creado.InmuebleTypeID = inmueble_type
                inmueble_creado.TipologiaID = tipologia
                inmueble_creado.EtapaID = instance
                inmueble_creado.EdificioID = edificio
                inmueble_creado.InmuebleStateID = inmueble_state
                inmueble_creado.Number = inmueble_data['Number']
                inmueble_creado.Floor = inmueble_data['Floor']
                inmueble_creado.BathroomQuantity = inmueble_data['BathroomQuantity']
                inmueble_creado.BedroomsQuantity = inmueble_data['BedroomsQuantity']
                inmueble_creado.UtilSquareMeters = inmueble_data['UtilSquareMeters']
                inmueble_creado.TerraceSquareMeters = inmueble_data['TerraceSquareMeters']
                inmueble_creado.LodgeSquareMeters = inmueble_data['LodgeSquareMeters']
                inmueble_creado.TotalSquareMeters = 0
                inmueble_creado.IsNotUsoyGoce = inmueble_data['IsNotUsoyGoce']
                inmueble_creado.Price = inmueble_data['Price']
                inmueble_creado.MaximunDiscount = maximun_discount
                inmueble_creado.CotizacionDuration = proyecto.CotizacionDuration

                for orientation_data in inmueble_data['OrientationID']:
                    orientations_uuid.append(orientation_data['OrientationID'])

                inmuebles_orientation[inmueble_creado.InmuebleID] = orientations_uuid

                inmuebles_creados.append(inmueble_creado)

                # Creacion de historial para inmuebles con edificio
                inmueble_hist = HistoricalInmueble()
                inmueble_hist.InmuebleTypeID = inmueble_type
                inmueble_hist.TipologiaID = tipologia
                inmueble_hist.EtapaID = etapa_hist
                inmueble_hist.EdificioID = edificio_hist
                inmueble_hist.InmuebleStateID = inmueble_state
                inmueble_hist.Number = inmueble_data['Number']
                inmueble_hist.Floor = inmueble_data['Floor']
                inmueble_hist.BathroomQuantity = inmueble_data['BathroomQuantity']
                inmueble_hist.BedroomsQuantity = inmueble_data['BedroomsQuantity']
                inmueble_hist.UtilSquareMeters = inmueble_data['UtilSquareMeters']
                inmueble_hist.TerraceSquareMeters = inmueble_data['TerraceSquareMeters']
                inmueble_hist.LodgeSquareMeters = inmueble_data['LodgeSquareMeters']
                inmueble_hist.TotalSquareMeters = 0
                inmueble_hist.IsNotUsoyGoce = inmueble_data['IsNotUsoyGoce']
                inmueble_hist.Price = inmueble_data['Price']
                inmueble_hist.MaximunDiscount = maximun_discount
                inmueble_hist.CotizacionDuration = proyecto.CotizacionDuration

                historicos.append(inmueble_hist)

            Inmueble.objects.bulk_create(inmuebles_creados)
            HistoricalInmueble.objects.bulk_create(historicos)

        revisar_numeros_duplicados(inmuebles_sin_edificio_data, None)

        inmuebles_creados = list()
        historicos = list()
        inmuebles_orientation_sin_edificio = dict()
        orientations_uuid_sin_edificio = list()

        for inmueble_data in inmuebles_sin_edificio_data:
            inmueble_type = InmuebleType.objects.get(
                InmuebleTypeID=inmueble_data['InmuebleTypeID'])
            tipologia_id = inmueble_data['TipologiaID']
            maximun_discount = inmueble_data['MaximunDiscount']

            if tipologia_id:
                tipologia = Tipologia.objects.get(
                    TipologiaID=tipologia_id)
            else:
                tipologia = None

            if not maximun_discount:
                maximun_discount = None

            if inmueble_type.Name == constants.INMUEBLE_TYPE[0] and not tipologia_id:
                raise CustomValidation(
                    "Los departamentos deben tener tipología",
                    status_code=status.HTTP_409_CONFLICT)

            inmueble_state = InmuebleState.objects.get(
                InmuebleStateID=inmueble_data['InmuebleStateID'])

            inmueble_creado = Inmueble()
            inmueble_creado.InmuebleTypeID = inmueble_type
            inmueble_creado.TipologiaID = tipologia
            inmueble_creado.EtapaID = instance
            inmueble_creado.EdificioID = None
            inmueble_creado.InmuebleStateID = inmueble_state
            inmueble_creado.Number = inmueble_data['Number']
            inmueble_creado.Floor = inmueble_data['Floor']
            inmueble_creado.BathroomQuantity = inmueble_data['BathroomQuantity']
            inmueble_creado.BedroomsQuantity = inmueble_data['BedroomsQuantity']
            inmueble_creado.UtilSquareMeters = inmueble_data['UtilSquareMeters']
            inmueble_creado.TerraceSquareMeters = inmueble_data['TerraceSquareMeters']
            inmueble_creado.LodgeSquareMeters = inmueble_data['LodgeSquareMeters']
            inmueble_creado.TotalSquareMeters = 0
            inmueble_creado.IsNotUsoyGoce = inmueble_data['IsNotUsoyGoce']
            inmueble_creado.Price = inmueble_data['Price']
            inmueble_creado.MaximunDiscount = maximun_discount
            inmueble_creado.CotizacionDuration = proyecto.CotizacionDuration

            if inmueble_data.get('OrientationID'):
                for orientation_data in inmueble_data['OrientationID']:
                    orientations_uuid_sin_edificio.append(orientation_data['OrientationID'])

            inmuebles_orientation_sin_edificio[inmueble_creado.InmuebleID] = orientations_uuid_sin_edificio

            inmuebles_creados.append(inmueble_creado)

            # Creacion de historial para inmuebles con edificio
            inmueble_hist = HistoricalInmueble()
            inmueble_hist.InmuebleTypeID = inmueble_type
            inmueble_hist.TipologiaID = tipologia
            inmueble_hist.EtapaID = etapa_hist
            inmueble_hist.EdificioID = None
            inmueble_hist.InmuebleStateID = inmueble_state
            inmueble_hist.Number = inmueble_data['Number']
            inmueble_hist.Floor = inmueble_data['Floor']
            inmueble_hist.BathroomQuantity = inmueble_data['BathroomQuantity']
            inmueble_hist.BedroomsQuantity = inmueble_data['BedroomsQuantity']
            inmueble_hist.UtilSquareMeters = inmueble_data['UtilSquareMeters']
            inmueble_hist.TerraceSquareMeters = inmueble_data['TerraceSquareMeters']
            inmueble_hist.LodgeSquareMeters = inmueble_data['LodgeSquareMeters']
            inmueble_hist.TotalSquareMeters = 0
            inmueble_hist.IsNotUsoyGoce = inmueble_data['IsNotUsoyGoce']
            inmueble_hist.Price = inmueble_data['Price']
            inmueble_hist.MaximunDiscount = maximun_discount
            inmueble_hist.CotizacionDuration = proyecto.CotizacionDuration

            historicos.append(inmueble_hist)

        Inmueble.objects.bulk_create(inmuebles_creados)
        HistoricalInmueble.objects.bulk_create(historicos)

        # Agregar orientaciones a inmuebles con edificios
        uuids_list = [key for key in inmuebles_orientation]

        inmuebles_orientations = Inmueble.objects.filter(InmuebleID__in=uuids_list)
        inms = list()
        for i in inmuebles_orientation:
            inmueble_ori = get_object_or_404(inmuebles_orientations, InmuebleID=i)
            for orientation_id in inmuebles_orientation[i]:
                orientation = get_object_or_404(Orientation, OrientationID=orientation_id)
                inmueble_ori.OrientationID.add(orientation)
            inms.append(inmueble_ori)

        bulk_update(inms)

        # Agregar orientaciones a inmuebles sin edificios
        uuids_list = [key for key in inmuebles_orientation_sin_edificio]

        inmuebles_orientations = Inmueble.objects.filter(InmuebleID__in=uuids_list)
        inms = list()
        for i in inmuebles_orientation_sin_edificio:
            inmueble_ori = get_object_or_404(inmuebles_orientations, InmuebleID=i)
            for orientation_id in inmuebles_orientation_sin_edificio[i]:
                orientation = get_object_or_404(Orientation, OrientationID=orientation_id)
                inmueble_ori.OrientationID.add(orientation)
            inms.append(inmueble_ori)

        bulk_update(inms)

        # Lo mismo que el anterior optimizar renderizacion de pdf de bitacora

        # # Bitacora
        # inmuebles = Inmueble.objects.filter(EtapaID=instance)
        # context_dict = {
        #     'etapa': instance,
        #     'inmuebles': inmuebles
        # }
        #
        # pdf = render_create_etapa_to_pdf(context_dict)
        #
        # pdf_generated = ContentFile(pdf)
        # pdf_generated.name = "Documento.pdf"

        proyecto_log_type = ProyectoLogType.objects.get(
            Name=constants.PROYECTO_LOG_TYPE[2])

        comment = "Proyecto modificado, se creo %s" % (instance.Name)

        ProyectoLog.objects.create(
            UserID=current_user,
            ProyectoID=proyecto,
            ProyectoLogTypeID=proyecto_log_type,
            Comment=comment,
            # Counter=counter.Count,
            # ProyectoDetailDocument=pdf_generated
        )

        counter.Count += 1
        counter.save()

        # Crear Notificacion Etapa sin fecha de ventas
        user_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])

        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=proyecto, UserProyectoTypeID=user_proyecto_type)

        # Permiso Monitorea Proyectos
        permission = Permission.objects.get(Name=constants.PERMISSIONS[14])

        usuarios_monitorea_proyectos = User.objects.filter(
            RoleID__PermissionID=permission
        )
        if not sales_start_date:
            crear_notificacion_etapa_sin_fecha_de_ventas(
                instance, current_user, jefe_proyecto, usuarios_monitorea_proyectos)

        eliminar_notificacion_proyecto_sin_inmuebles(proyecto)

        return instance

# Serializador para la creacion masiva de inmuebles desde un excel


class CreateMassiveEtapaInmueblesSerializer(serializers.ModelSerializer):
    File = serializers.FileField(
        required=False
    )

    class Meta:
        model = Etapa
        fields = ('File',)

    def save_db(self, instance, initial_data):
        current_user = return_current_user(self)

        proyecto = Proyecto.objects.get(
            ProyectoID=instance.ProyectoID.ProyectoID
        )

        # proyecto historico para historial de etapa
        counter = CounterHistory.objects.get(ProyectoID=proyecto)

        proyecto_hist = HistoricalProyecto.objects.create(
            ProyectoID=proyecto.ProyectoID,
            Counter=counter.Count,
            Name=proyecto.Name,
            Symbol=proyecto.Symbol,
            Address=proyecto.Address,
            InstitucionFinancieraID=proyecto.InstitucionFinancieraID,
            ComunaID=proyecto.ComunaID,
            InmobiliariaID=proyecto.InmobiliariaID,
            ConstructoraID=proyecto.ConstructoraID,
            CotizacionDuration=proyecto.CotizacionDuration,
            GuaranteeAmount=proyecto.GuaranteeAmount,
            PlanMediosState=proyecto.PlanMediosState,
            BorradorPromesaState=proyecto.BorradorPromesaState,
            IngresoComisionesState=proyecto.IngresoComisionesState
        )
        etapa_hist = HistoricalEtapa.objects.create(
            Name=instance.Name,
            SalesStartDate=instance.SalesStartDate,
            EtapaStateID=instance.EtapaStateID,
            ProyectoID=proyecto_hist,
        )

        inmuebles = Inmueble.objects.filter(EtapaID=instance)
        if inmuebles.exists():
            inmuebles.delete()

        historicos = list()
        inmuebles = list()
        orientaciones_in = dict()

        for inmueble in initial_data.get('data', []):
            edificio = None
            edificio_hist = None
            if inmueble.get('Edificio'):
                edificio = get_or_none(Edificio, Name=inmueble.get('Edificio'),
                                       EtapaID=instance)
                if not edificio:
                    edificio = Edificio.objects.create(
                        Name=inmueble.get('Edificio'),
                        EtapaID=instance
                    )
                    # creacion de historial para edificio
                    edificio_hist = HistoricalEdificio.objects.create(
                        Name=inmueble.get('Edificio'),
                        EtapaID=etapa_hist,
                    )

            number = inmueble.get('Numero')

            floor = inmueble.get('Piso')

            bathrooms_quantity = inmueble.get('CantidadBanos')

            bedrooms_quantity = inmueble.get('CantidadHabitaciones')

            util_square_meters = inmueble.get('MetrosCuadradosInterior')
            terrace_square_meters = inmueble.get('MetrosCuadradosTerraza')
            lodge_square_meters = inmueble.get('MetrosCuadradosLogia')
            orientacion = inmueble.get('Orientacion')
            # total_square_meters = inmueble.MetrosCuadradosTotales
            uso_goce = inmueble.get('UsoyGoce')
            price = inmueble.get('Precio')

            max_discount = inmueble.get('DescuentoMaximo')

            try:
                inmueble_type = InmuebleType.objects.get(Name=inmueble.get('TipoInmueble'))
            except:
                raise ValidationError("Unknown inmueble type named %s" % inmueble.get('TipoInmueble'))

            tipologia_name = inmueble.get('Tipologia')

            if inmueble_type.Name == constants.INMUEBLE_TYPE[0]:
                pass

            if inmueble_type.Name == constants.INMUEBLE_TYPE[0] and tipologia_name == 'No aplica':
                raise CustomValidation(
                    "Los departamentos deben tener tipología",
                    status_code=status.HTTP_409_CONFLICT)

            if not tipologia_name == 'No aplica':
                try:
                    tipologia = Tipologia.objects.get(
                        Name=tipologia_name)
                except:
                    # raise ValidationError("Unknown tipologia named %s" % tipologia_name)
                    tipologia = None
            else:
                tipologia = None
            try:
                inmueble_state = InmuebleState.objects.get(Name=inmueble.get('Estado'))
            except:
                raise ValidationError("Unknown inmueble state named %s" % inmueble.get('Estado'))

            if uso_goce == 'Sí':
                uso_goce = True
            else:
                uso_goce = False

            inmueble_creado = Inmueble()
            inmueble_creado.InmuebleID = uuid.uuid4()
            inmueble_creado.InmuebleTypeID = inmueble_type
            inmueble_creado.TipologiaID = tipologia
            inmueble_creado.EtapaID = instance
            inmueble_creado.EdificioID = edificio
            inmueble_creado.InmuebleStateID = inmueble_state
            inmueble_creado.Number = number
            inmueble_creado.Floor = floor
            inmueble_creado.BathroomQuantity = bathrooms_quantity
            inmueble_creado.BedroomsQuantity = bedrooms_quantity
            inmueble_creado.UtilSquareMeters = util_square_meters
            inmueble_creado.TerraceSquareMeters = terrace_square_meters
            inmueble_creado.LodgeSquareMeters = lodge_square_meters
            inmueble_creado.TotalSquareMeters = 0
            inmueble_creado.IsNotUsoyGoce = uso_goce
            inmueble_creado.Price = price
            inmueble_creado.MaximunDiscount = max_discount
            inmueble_creado.CotizacionDuration = proyecto.CotizacionDuration

            orientaciones_in[inmueble_creado.InmuebleID] = orientacion

            inmuebles.append(inmueble_creado)

            inmueble_hist = HistoricalInmueble()
            inmueble_hist.InmuebleID = uuid.uuid4()
            inmueble_hist.InmuebleTypeID = inmueble_type
            inmueble_hist.TipologiaID = tipologia
            inmueble_hist.EtapaID = etapa_hist
            inmueble_hist.EdificioID = edificio_hist
            inmueble_hist.InmuebleStateID = inmueble_state
            inmueble_hist.Number = number
            inmueble_hist.Floor = floor
            inmueble_hist.BathroomQuantity = bathrooms_quantity
            inmueble_hist.BedroomsQuantity = bedrooms_quantity
            inmueble_hist.UtilSquareMeters = util_square_meters
            inmueble_hist.TotalSquareMeters = 0
            inmueble_hist.IsNotUsoyGoce = uso_goce
            inmueble_hist.Price = price
            inmueble_hist.MaximunDiscount = max_discount
            inmueble_hist.CotizacionDuration = proyecto.CotizacionDuration

            orientaciones_in[inmueble_creado.InmuebleID] = orientacion

            historicos.append(inmueble_hist)

        Inmueble.objects.bulk_create(inmuebles)
        HistoricalInmueble.objects.bulk_create(historicos)

        # Bitacora
        inmuebles = Inmueble.objects.filter(EtapaID=instance)

        insert_properties_orientaations(
            inmuebles,
            orientaciones_in,
            "empresas_and_proyectos_inmueble_OrientationID")

        historicos = HistoricalInmueble.objects.filter(EtapaID=etapa_hist)

        insert_properties_orientaations(
            historicos,
            orientaciones_in,
            "history_historicalinmueble_OrientationID")

        context_dict = {
            'etapa': instance,
            'inmuebles': inmuebles
        }

        pdf = render_create_etapa_to_pdf(context_dict)

        pdf_generated = ContentFile(pdf)
        pdf_generated.name = "Documento.pdf"

        proyecto_log_type = ProyectoLogType.objects.get(
            Name=constants.PROYECTO_LOG_TYPE[2])

        comment = "Proyecto modificado, se creo %s vía excel" % (instance.Name)

        ProyectoLog.objects.create(
            UserID=current_user,
            ProyectoID=proyecto,
            ProyectoLogTypeID=proyecto_log_type,
            Comment=comment,
            Counter=counter.Count,
            ProyectoDetailDocument=pdf_generated
        )

        counter.Count += 1
        counter.save()

        eliminar_notificacion_proyecto_sin_inmuebles(proyecto)

        return instance

    @staticmethod
    def upload(instance, validated_data):
        proyecto = Proyecto.objects.get(
            ProyectoID=instance.ProyectoID.ProyectoID
        )
        file = validated_data['File']

        data = import_excel_inmuebles(file)

        revisar_numeros_duplicados_excel(data.iloc[1:].itertuples())

        inmuebles = list()
        inmueble_types = InmuebleType.objects.all()
        inmueble_states = InmuebleState.objects.all()

        for inmueble in data.iloc[1:].itertuples():
            if not is_nan(inmueble.Numero):
                number = inmueble.Numero
            else:
                number = None

            if not is_nan(inmueble.Piso):
                floor = inmueble.Piso
            else:
                floor = None

            if not is_nan(inmueble.CantidadBanos):
                bathrooms_quantity = inmueble.CantidadBanos
            else:
                bathrooms_quantity = None

            if not is_nan(inmueble.CantidadHabitaciones):
                bedrooms_quantity = inmueble.CantidadHabitaciones
            else:
                bedrooms_quantity = None

            util_square_meters = inmueble.MetrosCuadradosInterior
            terrace_square_meters = inmueble.MetrosCuadradosTerraza
            lodge_square_meters = inmueble.MetrosCuadradosLogia
            orientacion = inmueble.Orientacion
            # total_square_meters = inmueble.MetrosCuadradosTotales
            uso_goce = inmueble.UsoyGoce
            price = inmueble.Precio

            if not is_nan(inmueble.DescuentoMaximo):
                max_discount = inmueble.DescuentoMaximo
            else:
                max_discount = None

            try:
                inmueble_type = inmueble_types.get(Name=inmueble.TipoInmueble)
            except InmuebleType.DoesNotExist:
                raise ValidationError("Unknown inmueble type named %s" % inmueble.TipoInmueble)

            tipologia_name = inmueble.Tipologia

            if inmueble_type.Name == constants.INMUEBLE_TYPE[0] and tipologia_name == 'No aplica':
                raise CustomValidation(
                    "Los departamentos deben tener tipología",
                    status_code=status.HTTP_409_CONFLICT)
            try:
                inmueble_states.get(Name=inmueble.Estado)
            except InmuebleState.DoesNotExist:
                raise ValidationError("Unknown inmueble state named %s" % inmueble.Estado)

            if uso_goce == 'Sí':
                uso_goce = True
            else:
                uso_goce = False

            inmueble_creado = dict()
            inmueble_creado['TipoInmueble'] = inmueble.TipoInmueble if not is_nan(inmueble.TipoInmueble) else None
            inmueble_creado['Tipologia'] = tipologia_name if not is_nan(tipologia_name) else None
            inmueble_creado['Edificio'] = inmueble.Edificio if not is_nan(inmueble.Edificio) else None
            inmueble_creado['Estado'] = inmueble.Estado if not is_nan(inmueble.Estado) else None
            inmueble_creado['Numero'] = number
            inmueble_creado['Piso'] = floor
            inmueble_creado['CantidadBanos'] = bathrooms_quantity
            inmueble_creado['CantidadHabitaciones'] = bedrooms_quantity
            inmueble_creado['MetrosCuadradosInterior'] = util_square_meters
            inmueble_creado['MetrosCuadradosTerraza'] = terrace_square_meters
            inmueble_creado['MetrosCuadradosLogia'] = lodge_square_meters
            inmueble_creado['TotalSquareMeters'] = 0
            inmueble_creado['UsoyGoce'] = uso_goce
            inmueble_creado['Precio'] = price
            inmueble_creado['DescuentoMaximo'] = max_discount
            inmueble_creado['CotizacionDuration'] = proyecto.CotizacionDuration
            inmueble_creado['Orientacion'] = orientacion
            inmuebles.append(inmueble_creado)
        return inmuebles


class UpdateEtapaSerializer(serializers.ModelSerializer):
    EtapaID = serializers.UUIDField(
        write_only=True
    )
    EtapaStateID = serializers.UUIDField(
        write_only=True
    )
    SalesStartDate = serializers.DateTimeField(
        allow_null=True
    )

    class Meta:
        model = Etapa
        fields = ('EtapaID', 'EtapaStateID',
                  'Name', 'SalesStartDate')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        etapa_state_id = validated_data.pop('EtapaStateID')
        etapa_state = EtapaState.objects.get(EtapaStateID=etapa_state_id)
        sales_start_date = validated_data.get('SalesStartDate')

        proyecto = instance.ProyectoID

        # proyecto historico para historial de etapa
        counter = CounterHistory.objects.get(ProyectoID=proyecto)
        proyecto_hist = HistoricalProyecto.objects.create(
            ProyectoID=proyecto.ProyectoID,
            Counter=counter.Count,
            Name=proyecto.Name,
            Symbol=proyecto.Symbol,
            Address=proyecto.Address,
            InstitucionFinancieraID=proyecto.InstitucionFinancieraID,
            ComunaID=proyecto.ComunaID,
            InmobiliariaID=proyecto.InmobiliariaID,
            ConstructoraID=proyecto.ConstructoraID,
            CotizacionDuration=proyecto.CotizacionDuration,
            GuaranteeAmount=proyecto.GuaranteeAmount,
            PlanMediosState=proyecto.PlanMediosState,
            BorradorPromesaState=proyecto.BorradorPromesaState,
            IngresoComisionesState=proyecto.IngresoComisionesState
        )

        # creacion de historial para etapa
        etapa_hist = HistoricalEtapa.objects.create(
            Name=validated_data.get('Name', instance.Name),
            SalesStartDate=sales_start_date,
            EtapaStateID=etapa_state,
            ProyectoID=proyecto_hist
        )

        instance.Name = validated_data.get('Name', instance.Name)
        instance.SalesStartDate = sales_start_date
        instance.EtapaStateID = etapa_state

        proyecto_log_type = ProyectoLogType.objects.get(
            Name=constants.PROYECTO_LOG_TYPE[2])

        comment = "Proyecto modificado, se modifico %s" % (instance.Name)

        ProyectoLog.objects.create(
            UserID=current_user,
            ProyectoID=proyecto,
            ProyectoLogTypeID=proyecto_log_type,
            Counter=counter.Count,
            Comment=comment,
        )

        counter.Count += 1
        counter.save()

        instance.save()

        return instance
