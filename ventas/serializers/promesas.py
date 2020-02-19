from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers, status

from common import constants
from common.notifications import crear_notificacion_promesa_creada, crear_notificacion_maqueta_jp_aprobada, \
    crear_notificacion_maqueta_aprobada, \
    crear_notificacion_maqueta_rechazada, crear_notificacion_promesa_aprobada, crear_notificacion_promesa_rechazada, \
    crear_notificacion_promesa_enviada_a_inmobiliaria, crear_notificacion_copias_enviadas, \
    crear_notificacion_promesa_modificada, \
    crear_notificacion_promesa_envio_a_negociacion, \
    crear_notificacion_promesa_control_negociacion, \
    crear_notificacion_promesa_aprobada_negociacion, \
    crear_notificacion_promesa_rechazada_negociacion
from common.services import get_full_path_x, return_current_user
from common.validations import CustomValidation
from empresas_and_proyectos.models.inmuebles import Inmueble, InmuebleState
from empresas_and_proyectos.models.proyectos import UserProyectoType, UserProyecto, Proyecto
from users.models import User, Permission
from users.serializers.users import UserProfileSerializer
from ventas.models.clientes import Cliente
from ventas.models.conditions import Condition
from ventas.models.documents import DocumentVenta
from ventas.models.facturas import FacturaInmueble, ComisionInmobiliaria, Factura
from ventas.models.ofertas import Oferta
from ventas.models.patrimonies import Patrimony
from ventas.models.payment_forms import PayType
from ventas.models.promesas import Promesa, PromesaInmueble
from ventas.models.reservas import Reserva
from ventas.models.ventas_logs import VentaLog, VentaLogType
from ventas.serializers.clientes import ClienteSerializer
from ventas.serializers.conditions import (
    ConditionSerializer,
    CreateConditionSerializer,
    ApproveConditionSerializer)
from ventas.serializers.cotizaciones import ListCotizacionesInmueblesSerializer
from ventas.serializers.cuotas import ListCuotaSerializer
from ventas.serializers.documents_venta import DocumentVentaSerializer
from ventas.serializers.facturas import RetrieveFacturaSerializer
from ventas.serializers.patrimonies import PatrimonySerializer
from ventas.serializers.reservas import CreateReservaInmuebleSerializer, ListReservaInmuebleSerializer


def create_promesa(proyecto, cliente, vendedor, codeudor, inmuebles, folio, cotizacion_type, payment_firma_promesa,
                   payment_firma_escritura, payment_firma_institucion_financiera, ahorro_plus, paytype, current_user):
    instance = Promesa.objects.create(
        ProyectoID=proyecto,
        CotizacionTypeID=cotizacion_type,
        ClienteID=cliente,
        VendedorID=vendedor,
        CodeudorID=codeudor,
        Folio=folio,
        PromesaState=constants.PROMESA_STATE[0],
        PaymentFirmaPromesa=payment_firma_promesa,
        PaymentFirmaEscritura=payment_firma_escritura,
        PaymentInstitucionFinanciera=payment_firma_institucion_financiera,
        AhorroPlus=ahorro_plus,
        PayTypeID=paytype
    )

    inmuebles_promesa = list()

    for inmueble in inmuebles:
        inmueble_promesa = PromesaInmueble()
        inmueble_promesa.PromesaID = instance
        inmueble_promesa.InmuebleID = inmueble.InmuebleID
        inmueble_promesa.Discount = inmueble.Discount
        inmuebles_promesa.append(inmueble_promesa)

    PromesaInmueble.objects.bulk_create(inmuebles_promesa)

    venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[17])

    comment = "Creacion: Promesa {0} proyecto {1}".format(instance.Folio, proyecto.Name)

    VentaLog.objects.create(
        VentaID=instance.PromesaID,
        Folio=folio,
        UserID=current_user,
        ClienteID=cliente,
        ProyectoID=instance.ProyectoID,
        VentaLogTypeID=venta_log_type,
        Comment=comment,
    )

    # Crear notificaciones
    # Tipos de Usuarios
    vendedor_type = UserProyectoType.objects.get(
        Name=constants.USER_PROYECTO_TYPE[2])

    jefe_proyecto_type = UserProyectoType.objects.get(
        Name=constants.USER_PROYECTO_TYPE[1])

    # Usuarios
    jefe_proyecto = UserProyecto.objects.filter(
        ProyectoID=proyecto,
        UserProyectoTypeID=jefe_proyecto_type)

    vendedor = UserProyecto.objects.filter(
        ProyectoID=proyecto,
        UserProyectoTypeID=vendedor_type)

    permission = Permission.objects.get(Name=constants.PERMISSIONS[22])

    usuarios_confecciona_maquetas = User.objects.filter(
        RoleID__PermissionID=permission
    )

    crear_notificacion_promesa_creada(
        instance, proyecto, jefe_proyecto, vendedor,
        usuarios_confecciona_maquetas)


class ListPromesaSerializer(serializers.ModelSerializer):
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )
    Proyecto = serializers.CharField(
        source='ProyectoID.Name'
    )
    ClienteID = serializers.UUIDField(
        source='ClienteID.UserID'
    )
    Cliente = ClienteSerializer(
        source='ClienteID',
        allow_null=True
    )
    Inmuebles = serializers.SerializerMethodField('get_inmuebles')
    Factura = serializers.SerializerMethodField('get_factura')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ProyectoID', 'ClienteID')
        return queryset

    class Meta:
        model = Promesa
        fields = ('PromesaID', 'ProyectoID', 'Proyecto', 'ClienteID', 'Date',
                  'Cliente', 'Folio',
                  'PromesaDesistimientoState',
                  'PromesaResciliacionState',
                  'PromesaResolucionState',
                  'PromesaModificacionState',
                  'PromesaState', 'Inmuebles', 'Factura', 'AprobacionInmobiliaria')

    def get_inmuebles(self, obj):
        inmuebles_promesa = PromesaInmueble.objects.filter(
            PromesaID=obj)
        serializer = ListReservaInmuebleSerializer(
            instance=inmuebles_promesa, many=True)
        return serializer.data

    def get_factura(self, obj):
        factura = Factura.objects.filter(Folio=obj.Folio).first()
        if factura:
            serializer = RetrieveFacturaSerializer(instance=factura)
            return serializer.data
        else:
            return None


class RetrieveModifiedPromesaSerializer(serializers.ModelSerializer):
    ClienteID = serializers.UUIDField(
        source='ClienteID.UserID'
    )
    ClienteName = serializers.CharField(
        source='ClienteID.Name'
    )
    ClienteLastNames = serializers.CharField(
        source='ClienteID.LastNames'
    )
    ClienteRut = serializers.CharField(
        source='ClienteID.Rut'
    )
    CodeudorID = serializers.UUIDField(
        source='CodeudorID.UserID',
        allow_null=True
    )
    CodeudorName = serializers.CharField(
        source='CodeudorID.Name',
        allow_null=True
    )
    CodeudorLastNames = serializers.CharField(
        source='CodeudorID.LastNames',
        allow_null=True
    )
    CodeudorRut = serializers.CharField(
        source='CodeudorID.Rut',
        allow_null=True
    )
    PayType = serializers.CharField(
        source='PayTypeID.Name'
    )
    PaymentFirmaPromesa = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    PaymentFirmaEscritura = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    PaymentInstitucionFinanciera = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    AhorroPlus = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    Inmuebles = serializers.SerializerMethodField('get_inmuebles')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ProyectoID',
            'ClienteID',
            'VendedorID',
            'CodeudorID',
            'PayTypeID')
        queryset = queryset.prefetch_related('InmuebleID')
        return queryset

    class Meta:
        model = Promesa
        fields = ('ClienteID', 'ClienteName', 'ClienteLastNames',
                  'ClienteRut', 'CodeudorID', 'CodeudorName',
                  'CodeudorLastNames', 'CodeudorRut', 'PayType',
                  'Inmuebles', 'PaymentFirmaPromesa', 'PaymentFirmaEscritura',
                  'PaymentInstitucionFinanciera', 'AhorroPlus')

    def get_inmuebles(self, obj):
        inmuebles_promesa = PromesaInmueble.objects.filter(
            PromesaID=obj)
        serializer = ListCotizacionesInmueblesSerializer(
            instance=inmuebles_promesa, many=True)
        return serializer.data


class RetrievePromesaSerializer(serializers.ModelSerializer):
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )
    Proyecto = serializers.CharField(
        source='ProyectoID.Name'
    )
    Condition = CreateConditionSerializer(
        source='ConditionID',
        many=True,
        required=False
    )
    CotizacionType = serializers.CharField(
        source='CotizacionTypeID.Name',
        allow_null=True
    )
    ClienteID = serializers.UUIDField(
        source='ClienteID.UserID'
    )
    Cliente = ClienteSerializer(
        source='ClienteID',
        allow_null=True
    )
    VendedorID = serializers.UUIDField(
        source='VendedorID.UserID'
    )
    Vendedor = UserProfileSerializer(
        source='VendedorID',
        allow_null=True
    )
    CodeudorID = serializers.UUIDField(
        source='CodeudorID.UserID',
        allow_null=True
    )
    Codeudor = ClienteSerializer(
        source='CodeudorID',
        allow_null=True
    )
    PayType = serializers.CharField(
        source='PayTypeID.Name'
    )
    PaymentFirmaPromesa = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    PaymentFirmaEscritura = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    PaymentInstitucionFinanciera = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    AhorroPlus = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    Inmuebles = serializers.SerializerMethodField('get_inmuebles')
    Documents = serializers.SerializerMethodField('get_documents')
    DocumentPromesa = serializers.SerializerMethodField(
        'get_document_promesa_url')
    DocumentPromesaFirma = serializers.SerializerMethodField(
        'get_document_promesa_firma_url')
    DocumentChequesFirma = serializers.SerializerMethodField(
        'get_document_cheques_firma_url')
    DocumentPlantaFirma = serializers.SerializerMethodField(
        'get_document_planta_firma_url')

    DocumentFirmaComprador = serializers.SerializerMethodField(
        'get_document_firma_comprador_url')
    DocumentPaymentForm = serializers.SerializerMethodField(
        'get_document_payment_form_url')
    DocumentResciliacion = serializers.SerializerMethodField(
        'get_DocumentResciliacion_url')
    DocumentResciliacionFirma = serializers.SerializerMethodField(
        'get_DocumentResciliacionFirma_url')
    DocumentResolucion = serializers.SerializerMethodField(
        'get_DocumentResolucion_url')
    # Modification = serializers.SerializerMethodField('get_promesa_modified')
    Patrimony = serializers.SerializerMethodField('get_patrimony')
    Cuotas = serializers.SerializerMethodField('get_cuotas')
    OfertaID = serializers.SerializerMethodField('get_oferta_id')
    Condition = serializers.SerializerMethodField('get_conditions')
    Factura = serializers.SerializerMethodField('get_factura')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ProyectoID',
            'ClienteID',
            'VendedorID',
            'CodeudorID',
            'PayTypeID')
        queryset = queryset.prefetch_related('InmuebleID')
        return queryset

    class Meta:
        model = Promesa
        fields = (
            'PromesaID',
            'ProyectoID',
            'Condition',
            'Proyecto',
            'CotizacionType',
            'ClienteID',
            'Cliente',
            'VendedorID',
            'Vendedor',
            'CodeudorID',
            'Codeudor',
            'Date',
            'DocumentPromesa',
            'DocumentPromesaFirma',
            'DocumentChequesFirma',
            'DocumentPlantaFirma',
            'DocumentFirmaComprador',
            'DocumentPaymentForm',
            'DocumentResciliacion',
            'DocumentResciliacionFirma',
            'DocumentResolucion',
            'DateEnvioPromesa',
            'DateRegresoPromesa',
            'DateLegalizacionPromesa',
            'DateEnvioCopias',
            'Folio',
            'PromesaState',
            'PromesaDesistimientoState',
            'PromesaResciliacionState',
            'PromesaResolucionState',
            'PromesaModificacionState',
            'PayType',
            'PaymentFirmaPromesa',
            'PaymentFirmaEscritura',
            'PaymentInstitucionFinanciera',
            'AhorroPlus',
            'Inmuebles',
            'Patrimony',
            'Cuotas',
            'Documents',
            'OfertaID',
            'Factura', 'AprobacionInmobiliaria',
            'FechaFirmaDeEscritura', 'FechaEntregaDeInmueble',
            'DesistimientoEspecial', 'ModificacionEnLaClausula', 'MetodoComunicacionEscrituracion', 'DatePayment')

    def get_inmuebles(self, obj):
        inmuebles_promesa = PromesaInmueble.objects.filter(
            PromesaID=obj)
        serializer = ListReservaInmuebleSerializer(
            instance=inmuebles_promesa, many=True)
        return serializer.data

    def get_documents(self, obj):
        try:
            documents = DocumentVenta.objects.get(
                Folio=obj.Folio)
            serializer = DocumentVentaSerializer(
                instance=documents, context={'url': self.context['request']})
            return serializer.data
        except DocumentVenta.DoesNotExist:
            return None

    def get_document_promesa_url(self, obj):
        if obj.DocumentPromesa:
            return "http://" + get_current_site(self.context.get('request')).domain + obj.DocumentPromesa.url
        else:
            return ""

    def get_document_promesa_firma_url(self, obj):
        if obj.DocumentPromesaFirma:
            return "http://" + get_current_site(self.context.get('request')).domain + obj.DocumentPromesaFirma.url
        else:
            return ""

    def get_document_cheques_firma_url(self, obj):
        if obj.DocumentChequesFirma:
            return "http://" + get_current_site(self.context.get('request')).domain + obj.DocumentChequesFirma.url
        else:
            return ""

    def get_document_planta_firma_url(self, obj):
        if obj.DocumentPlantaFirma:
            return "http://" + get_current_site(self.context.get('request')).domain + obj.DocumentPlantaFirma.url
        else:
            return ""

    def get_document_firma_comprador_url(self, obj):
        if obj.DocumentFirmaComprador:
            return "http://" + get_current_site(self.context.get('request')).domain + obj.DocumentFirmaComprador.url
        else:
            return ""

    def get_document_payment_form_url(self, obj):
        if obj.DocumentPaymentForm:
            return "http://" + get_current_site(self.context.get('request')).domain + obj.DocumentPaymentForm.url
        else:
            return ""

    def get_DocumentResciliacion_url(self, obj):
        if obj.DocumentResciliacion:
            return "http://" + get_current_site(self.context.get('request')).domain + obj.DocumentResciliacion.url
        else:
            return ""

    def get_DocumentResciliacionFirma_url(self, obj):
        if obj.DocumentResciliacionFirma:
            return "http://" + get_current_site(self.context.get('request')).domain + obj.DocumentResciliacionFirma.url
        else:
            return ""

    def get_DocumentResolucion_url(self, obj):
        if obj.DocumentResolucion:
            return "http://" + get_current_site(self.context.get('request')).domain + obj.DocumentResolucion.url
        else:
            return ""

    def get_promesa_modified(self, obj):
        try:
            modified = Promesa.objects.get(
                PromesaID=obj.PromesaModified.PromesaID)
            serializer = RetrieveModifiedPromesaSerializer(
                instance=modified)
            return serializer.data
        except AttributeError:
            return {}

    def get_patrimony(self, obj):
        reserva = Reserva.objects.filter(Folio=obj.Folio).first()
        patrimonies = Patrimony.objects.filter(ClienteID=reserva.ClienteID)
        if patrimonies.exists():
            return PatrimonySerializer(instance=patrimonies[0]).data
        return None

    def get_cuotas(self, obj):
        reserva = Reserva.objects.filter(Folio=obj.Folio).first()
        cuotas = reserva.CuotaID.all()
        serializer = ListCuotaSerializer(
            instance=cuotas, many=True)
        return serializer.data

    def get_oferta_id(self, obj):
        oferta = Oferta.objects.filter(Folio=obj.Folio).first()
        return oferta.OfertaID

    def get_conditions(self, obj):
        reserva = Reserva.objects.filter(Folio=obj.Folio).first()
        conditions = reserva.ConditionID.all()
        serializer = ConditionSerializer(
            instance=conditions, many=True)
        return serializer.data

    def get_factura(self, obj):
        factura = Factura.objects.filter(Folio=obj.Folio).first()
        if factura:
            serializer = RetrieveFacturaSerializer(instance=factura)
            return serializer.data
        else:
            return None


class ApproveMaquetaPromesaSerializer(serializers.ModelSerializer):
    PromesaState = serializers.CharField(
        read_only=True
    )
    Comment = serializers.CharField(
        write_only=True,
        allow_blank=True
    )
    Resolution = serializers.BooleanField(
        write_only=True
    )

    class Meta:
        model = Promesa
        fields = ('PromesaState', 'Resolution', 'Comment')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        resolution = validated_data.pop('Resolution')
        comment = validated_data.pop('Comment')

        if resolution:
            if instance.PromesaState == constants.PROMESA_STATE[1]:
                raise CustomValidation(
                    "Maqueta promesa ya ha sido aprobada",
                    status_code=status.HTTP_409_CONFLICT)

            # Tipos de Usuario
            vendedor_type = UserProyectoType.objects.get(
                Name=constants.USER_PROYECTO_TYPE[2])
            jefe_proyecto_type = UserProyectoType.objects.get(
                Name=constants.USER_PROYECTO_TYPE[1])

            # Usuarios
            vendedor = UserProyecto.objects.filter(
                ProyectoID=instance.ProyectoID,
                UserProyectoTypeID=vendedor_type)
            jefe_proyecto = UserProyecto.objects.filter(
                ProyectoID=instance.ProyectoID,
                UserProyectoTypeID=jefe_proyecto_type)
            # if AC approves, move to JP to approve
            if instance.PromesaState == constants.PROMESA_STATE[9]:
                instance.PromesaState = constants.PROMESA_STATE[11]
                venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[31])
                crear_notificacion_maqueta_jp_aprobada(instance, jefe_proyecto)
            # AC approve has approved and now JP approves, move to 'Pendiente firma comprador'
            else:
                instance.PromesaState = constants.PROMESA_STATE[1]
                venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[18])
                crear_notificacion_maqueta_aprobada(instance, vendedor)
        else:
            # Tipos de Usuario
            permission = Permission.objects.get(Name=constants.PERMISSIONS[22])
            # Usuarios
            usuarios_confecciona_maquetas = User.objects.filter(
                RoleID__PermissionID=permission)

            instance.PromesaState = constants.PROMESA_STATE[0]
            venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[19])

            crear_notificacion_maqueta_rechazada(instance, usuarios_confecciona_maquetas)

        VentaLog.objects.create(
            VentaID=instance.PromesaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment,
        )

        instance.save()

        return instance


class ControlPromesaSerializer(serializers.ModelSerializer):
    PromesaState = serializers.CharField(
        read_only=True
    )

    Comment = serializers.CharField(
        write_only=True,
        allow_blank=True
    )

    Condition = CreateConditionSerializer(
        source='ConditionID',
        many=True,
        required=False
    )

    Resolution = serializers.BooleanField(
        write_only=True
    )

    class Meta:
        model = Promesa
        fields = ('PromesaState', 'Resolution', 'Comment', 'Condition')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        conditions_data = validated_data.get('ConditionID', False)
        comment = validated_data.pop('Comment')
        resolution = validated_data.pop('Resolution')

        # Usuarios
        vendedor_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[2])

        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])

        # Usuarios
        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=jefe_proyecto_type)

        vendedor = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=vendedor_type)

        if resolution:
            if instance.PromesaState == constants.PROMESA_STATE[2]:
                raise CustomValidation(
                    "Promesa ya ha sido aprobada",
                    status_code=status.HTTP_409_CONFLICT)

            if instance.PromesaState == constants.PROMESA_STATE[0]:
                raise CustomValidation(
                    "Promesa debe estar en estado pendiente firma comprador",
                    status_code=status.HTTP_409_CONFLICT)

            venta_log_type = VentaLogType.objects.get(
                Name=constants.VENTA_LOG_TYPE[20])

            promesa_state = constants.PROMESA_STATE[2]
            inmuebles = PromesaInmueble.objects.filter(PromesaID=instance)

            for inmueble in inmuebles:
                inmueble_state = InmuebleState.objects.get(
                    Name=constants.INMUEBLE_STATE[3]
                )
                inmueble.InmuebleID.InmuebleStateID = inmueble_state
                inmueble.InmuebleID.save()

            if conditions_data is not False and conditions_data is not None:
                conditions = Condition.objects.filter(
                    condition_promesa=instance
                )
                if conditions.exists():
                    conditions.delete()

                instance.ConditionID.clear()

                for condition_data in conditions_data:
                    condition = Condition.objects.create(
                        Description=condition_data['Description']
                    )
                    instance.ConditionID.add(condition)
            elif conditions_data is None:
                conditions = Condition.objects.filter(
                    condition_promesa=instance
                )
                if conditions.exists():
                    conditions.delete()

                instance.ConditionID.clear()
            else:
                conditions = None

            crear_notificacion_promesa_aprobada(instance, instance.ProyectoID, jefe_proyecto, vendedor)

        else:
            if instance.PromesaState == constants.PROMESA_STATE[2]:
                raise CustomValidation(
                    "Promesa ya ha sido aprobada, no se puede rechazar",
                    status_code=status.HTTP_409_CONFLICT)

            venta_log_type = VentaLogType.objects.get(
                Name=constants.VENTA_LOG_TYPE[21])

            promesa_state = constants.PROMESA_STATE[1]
            crear_notificacion_promesa_rechazada(instance, instance.ProyectoID, jefe_proyecto, vendedor)

        VentaLog.objects.create(
            VentaID=instance.PromesaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment
        )

        instance.PromesaState = promesa_state
        instance.save()

        return instance


class RegisterSendPromesaToInmobiliariaSerializer(serializers.ModelSerializer):
    PromesaState = serializers.CharField(
        read_only=True
    )
    DateEnvioPromesa = serializers.DateTimeField(
        write_only=True
    )

    class Meta:
        model = Promesa
        fields = ('PromesaState', 'DateEnvioPromesa')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        date = validated_data.pop('DateEnvioPromesa')

        venta_log_type = VentaLogType.objects.get(
            Name=constants.VENTA_LOG_TYPE[22])

        # Tipos de Usuarios
        representante_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[0])

        aprobador_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[4])

        vendedor_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[2])

        # Usuarios
        representantes = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=representante_type)

        aprobadores = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=aprobador_type)

        vendedor = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=vendedor_type)

        instance.DateEnvioPromesa = date

        crear_notificacion_promesa_enviada_a_inmobiliaria(instance, instance.ProyectoID,
                                                          representantes, aprobadores, vendedor)

        comment = "Registro fecha envio promesa {folio} proyecto {nombre}".format(folio=instance.Folio,
                                                                                  nombre=instance.ProyectoID.Name)

        # Creacion de inmuebles por facturar
        inmuebles_promesa = PromesaInmueble.objects.filter(PromesaID=instance)

        inmuebles_a_facturar = list()

        for inmueble_promesa in inmuebles_promesa:
            discount = (inmueble_promesa.InmuebleID.Price * inmueble_promesa.Discount) / 100
            price = inmueble_promesa.InmuebleID.Price - discount
            comision = ComisionInmobiliaria.objects.get(ProyectoID=instance.ProyectoID)
            inmueble_a_facturar = FacturaInmueble()
            inmueble_a_facturar.InmuebleID = inmueble_promesa.InmuebleID
            inmueble_a_facturar.ProyectoID = instance.ProyectoID
            inmueble_a_facturar.FolioVenta = instance.Folio
            inmueble_a_facturar.Price = price
            inmueble_a_facturar.Comision = comision.PromesaFirmada
            inmueble_a_facturar.Tipo = constants.FACTURA_INMUEBLE_TYPE[0]
            inmueble_a_facturar.State = constants.FACTURA_INMUEBLE_STATE[0]

            inmuebles_a_facturar.append(inmueble_a_facturar)

        FacturaInmueble.objects.bulk_create(inmuebles_a_facturar)

        VentaLog.objects.create(
            VentaID=instance.PromesaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment
        )

        instance.PromesaState = constants.PROMESA_STATE[3]
        instance.save()

        return instance


## should remove
def generateFactura(promesa):
    factura = Factura.objects.filter(Folio=promesa.Folio)
    if len(factura) > 0:
        factura = factura[0]
    else:
        factura = Factura(
            FacturaState=constants.FACTURA_STATE[0],
            ProyectoID=promesa.ProyectoID,
            InmobiliariaID=promesa.ProyectoID.InmobiliariaID,
            Folio=promesa.Folio
        )
    factura.Value = promesa.PaymentFirmaPromesa
    factura.Number = factura.id
    factura.FacturaState = constants.FACTURA_STATE[0]
    factura.save()
    # update inmuebles por facturar
    FacturaInmueble.objects.filter(FolioVenta=promesa.Folio).update(
        FacturaID=factura.id
    )


class GenerateFacturaSerializer(serializers.ModelSerializer):
    PromesaState = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Promesa
        fields = ('PromesaState',)

    def update(self, instance, validated_data):
        # Create factura
        generateFactura(instance)

        instance.PromesaState = constants.PROMESA_STATE[4]
        instance.save()

        return instance


class RegisterSignatureInmobiliariaSerializer(serializers.ModelSerializer):
    PromesaState = serializers.CharField(
        read_only=True
    )
    DateRegresoPromesa = serializers.DateTimeField(
        write_only=True
    )

    class Meta:
        model = Promesa
        fields = ('PromesaState', 'DateRegresoPromesa')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        date = validated_data.pop('DateRegresoPromesa')

        venta_log_type = VentaLogType.objects.get(
            Name=constants.VENTA_LOG_TYPE[23])

        instance.DateRegresoPromesa = date

        comment = "Registro fecha firma inmobiliaria promesa {folio} proyecto {nombre}".format(
            folio=instance.Folio,
            nombre=instance.ProyectoID.Name)

        VentaLog.objects.create(
            VentaID=instance.PromesaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment
        )

        inmuebles = PromesaInmueble.objects.filter(PromesaID=instance).first()
        etapa = inmuebles.InmuebleID.EtapaID

        if etapa.EtapaStateID.Name == constants.ETAPA_STATE[2]:
            promesa_state = constants.PROMESA_STATE[6]
        else:
            promesa_state = constants.PROMESA_STATE[5]

        instance.PromesaState = promesa_state
        instance.save()

        return instance


class LegalizePromesaSerializer(serializers.ModelSerializer):
    PromesaState = serializers.CharField(
        read_only=True
    )
    DateLegalizacionPromesa = serializers.DateTimeField(
        write_only=True
    )

    class Meta:
        model = Promesa
        fields = ('PromesaState', 'DateLegalizacionPromesa')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        date = validated_data.pop('DateLegalizacionPromesa')

        inmuebles = PromesaInmueble.objects.filter(PromesaID=instance).first()
        etapa = inmuebles.InmuebleID.EtapaID

        if etapa.EtapaStateID.Name == constants.ETAPA_STATE[2]:
            raise CustomValidation(
                "Etapa en escrituración, no es posible legalizar promesa",
                status_code=status.HTTP_409_CONFLICT)

        venta_log_type = VentaLogType.objects.get(
            Name=constants.VENTA_LOG_TYPE[24])

        instance.DateLegalizacionPromesa = date

        comment = "Registro fecha legalizacion promesa {folio} proyecto {nombre}".format(
            folio=instance.Folio,
            nombre=instance.ProyectoID.Name)

        VentaLog.objects.create(
            VentaID=instance.PromesaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment
        )

        instance.PromesaState = constants.PROMESA_STATE[6]
        instance.save()

        return instance


class SendCopiesSerializer(serializers.ModelSerializer):
    PromesaState = serializers.CharField(
        read_only=True
    )
    DateEnvioCopias = serializers.DateTimeField(
        write_only=True
    )

    class Meta:
        model = Promesa
        fields = ('PromesaState', 'DateEnvioCopias')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        date = validated_data.pop('DateEnvioCopias')

        inmuebles = PromesaInmueble.objects.filter(PromesaID=instance).first()
        etapa = inmuebles.InmuebleID.EtapaID

        venta_log_type = VentaLogType.objects.get(
            Name=constants.VENTA_LOG_TYPE[25])

        instance.DateEnvioCopias = date
        comment = "Registro fecha envio copias promesa {folio} proyecto {nombre}".format(
            folio=instance.Folio,
            nombre=instance.ProyectoID.Name)

        VentaLog.objects.create(
            VentaID=instance.PromesaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment
        )

        if etapa.EtapaStateID.Name == constants.ETAPA_STATE[0] or etapa.EtapaStateID.Name == constants.ETAPA_STATE[1]:
            promesa_state = constants.PROMESA_STATE[7]
        elif etapa.EtapaStateID.Name == constants.ETAPA_STATE[2] or etapa.EtapaStateID.Name == constants.ETAPA_STATE[4]:
            promesa_state = constants.PROMESA_STATE[8]

        # Crear Notificacionea
        # Tipos de Usuarios
        representante_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[0])

        aprobador_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[4])

        vendedor_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[2])

        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])

        # Usuarios
        representantes = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=representante_type)

        aprobadores = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=aprobador_type)

        vendedor = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=vendedor_type)

        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=jefe_proyecto_type)

        crear_notificacion_copias_enviadas(instance, instance.ProyectoID, representantes, aprobadores,
                                           jefe_proyecto, vendedor)

        instance.PromesaState = promesa_state
        instance.save()
        # generateFactura(instance)

        return instance


# Serializador para modificar promesa despues de ingresada la firma del comprador
class ModifiedPromesaSerializer(serializers.ModelSerializer):
    ClienteID = serializers.UUIDField(
        write_only=True
    )
    CodeudorID = serializers.UUIDField(
        write_only=True,
        allow_null=True
    )
    PayType = serializers.CharField(
        write_only=True
    )
    Inmuebles = CreateReservaInmuebleSerializer(
        source='InmuebleID',
        many=True,
        write_only=True
    )
    PaymentFirmaPromesa = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
    )
    PaymentFirmaEscritura = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
    )
    PaymentInstitucionFinanciera = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True
    )
    AhorroPlus = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True
    )

    class Meta:
        model = Promesa
        fields = ('ClienteID', 'CodeudorID', 'PayType',
                  'Inmuebles', 'PaymentFirmaPromesa', 'PaymentFirmaEscritura',
                  'PaymentInstitucionFinanciera', 'AhorroPlus')


class UpdatePromesaSerializer(serializers.ModelSerializer):
    PromesaState = serializers.CharField(
        read_only=True
    )
    PromesaModified = ModifiedPromesaSerializer(
        write_only=True
    )

    class Meta:
        model = Promesa
        fields = ('PromesaState', 'PromesaModified')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        if (instance.PromesaState == constants.PROMESA_STATE[0] or
                instance.PromesaState == constants.PROMESA_STATE[1] or
                instance.PromesaState == constants.PROMESA_STATE[9] or
                instance.PromesaState == constants.PROMESA_STATE[11]):

            oferta = Oferta.objects.get(Folio=instance.Folio)
            oferta.OfertaState = constants.OFERTA_STATE[0]
            oferta.save()
            inmuebles = PromesaInmueble.objects.filter(PromesaID=instance)

            if inmuebles.exists():
                inmuebles.delete()

            venta_log_type = VentaLogType.objects.get(
                Name=constants.VENTA_LOG_TYPE[26])

            comment = "Modificacion promesa {folio} proyecto {nombre} antes de la firma comprador".format(
                folio=instance.Folio,
                nombre=instance.ProyectoID.Name)
        else:
            promesa_modified_data = validated_data.pop('PromesaModified')
            cliente = Cliente.objects.get(UserID=promesa_modified_data.get('ClienteID'))

            if promesa_modified_data.get('CodeudorID'):
                codeudor = Cliente.objects.get(UserID=promesa_modified_data.get('CodeudorID'))
            else:
                codeudor = None

            paytype = PayType.objects.get(Name=promesa_modified_data.get('PayType'))

            promesa_modified = Promesa.objects.create(
                ProyectoID=instance.ProyectoID,
                ClienteID=cliente,
                CodeudorID=codeudor,
                VendedorID=instance.VendedorID,
                PayTypeID=paytype,
                PaymentFirmaPromesa=promesa_modified_data.get('PaymentFirmaPromesa'),
                PaymentFirmaEscritura=promesa_modified_data.get('PaymentFirmaEscritura'),
                PaymentInstitucionFinanciera=promesa_modified_data.get('PaymentInstitucionFinanciera'),
                AhorroPlus=promesa_modified_data.get('AhorroPlus'),
                IsOfficial=False
            )

            instance.PromesaModified = promesa_modified
            instance.PromesaState = constants.PROMESA_STATE[10]
            instance.save()

            venta_log_type = VentaLogType.objects.get(
                Name=constants.VENTA_LOG_TYPE[27])

            comment = "Modificacion promesa {folio} proyecto {nombre} despues de la firma comprador".format(
                folio=instance.Folio,
                nombre=instance.ProyectoID.Name)
            # Crear Notificaciones

            jefe_proyecto_type = UserProyectoType.objects.get(
                Name=constants.USER_PROYECTO_TYPE[1])

            jefe_proyecto = UserProyecto.objects.filter(
                ProyectoID=instance.ProyectoID,
                UserProyectoTypeID=jefe_proyecto_type)

            crear_notificacion_promesa_modificada(instance, instance.ProyectoID, jefe_proyecto)

        VentaLog.objects.create(
            VentaID=instance.PromesaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment
        )
        return instance


class UploadConfeccionPromesaSerializer(serializers.ModelSerializer):
    DocumentPromesa = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentPaymentForm = serializers.FileField(
        allow_empty_file=True,
        required=False
    )

    class Meta:
        model = Promesa
        fields = ('DocumentPromesa', 'PromesaState',
                  'FechaFirmaDeEscritura', 'FechaEntregaDeInmueble',
                  'DesistimientoEspecial', 'ModificacionEnLaClausula', 'MetodoComunicacionEscrituracion',
                  'DocumentPaymentForm', 'DatePayment')

    def update(self, instance, validated_data):
        if 'FechaFirmaDeEscritura' in validated_data:
            instance.FechaFirmaDeEscritura = validated_data['FechaFirmaDeEscritura']
        if 'FechaEntregaDeInmueble' in validated_data:
            instance.FechaEntregaDeInmueble = validated_data['FechaEntregaDeInmueble']
        instance.DesistimientoEspecial = validated_data['DesistimientoEspecial']
        instance.ModificacionEnLaClausula = validated_data['ModificacionEnLaClausula']
        instance.MetodoComunicacionEscrituracion = validated_data['MetodoComunicacionEscrituracion']
        if 'DatePayment' in validated_data:
            instance.DatePayment = validated_data['DatePayment']
        if 'DocumentPaymentForm' in validated_data:
            instance.DocumentPaymentForm = validated_data['DocumentPaymentForm']

        if 'DocumentPromesa' in validated_data:
            instance.DocumentPromesa = validated_data['DocumentPromesa']

        if instance.DocumentPromesa:
            instance.PromesaState = constants.PROMESA_STATE[9]

        instance.save()

        return instance


class UploadFirmaDocumentSerializer(serializers.ModelSerializer):
    DocumentPromesaFirma = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentChequesFirma = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentPlantaFirma = serializers.FileField(
        allow_empty_file=True,
        required=False
    )

    class Meta:
        model = Promesa
        fields = ('DocumentPromesaFirma', 'DocumentChequesFirma', 'DocumentPlantaFirma',
                  'PromesaState')

    def update(self, instance, validated_data):
        if 'DocumentPromesaFirma' in validated_data:
            instance.DocumentPromesaFirma = validated_data['DocumentPromesaFirma']
        if 'DocumentChequesFirma' in validated_data:
            instance.DocumentChequesFirma = validated_data['DocumentChequesFirma']
        if 'DocumentPlantaFirma' in validated_data:
            instance.DocumentPlantaFirma = validated_data['DocumentPlantaFirma']

        instance.PromesaState = constants.PROMESA_STATE[12]
        instance.save()
        return instance


class SendNegociacionJPSerializer(serializers.ModelSerializer):
    PromesaState = serializers.CharField(
        read_only=True
    )

    Condition = ConditionSerializer(
        required=False,
        many=True,
        allow_null=True,
        write_only=True
    )

    class Meta:
        model = Promesa
        fields = ('PromesaState', 'Condition')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        conditions_data = validated_data.pop('Condition')

        # Usuarios
        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])
        vendedor_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[2])
        # Usuarios
        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=jefe_proyecto_type)

        vendedor_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=vendedor_proyecto_type)

        reserva = Reserva.objects.get(Folio=instance.Folio)
        conditions = reserva.ConditionID.all()

        if conditions.exists():
            conditions.delete()

        reserva.ConditionID.clear()
        if conditions_data:
            for condition_data in conditions_data:
                condition = Condition.objects.create(
                    Description=condition_data['Description'],
                    IsImportant=condition_data.get('IsImportant', False),
                    IsApprove=condition_data.get('IsApprove', False)
                )
                reserva.ConditionID.add(condition)

        crear_notificacion_promesa_envio_a_negociacion(instance, instance.ProyectoID, jefe_proyecto, vendedor_proyecto)

        VentaLog.objects.create(
            VentaID=instance.PromesaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=VentaLogType.objects.get(
                Name=constants.VENTA_LOG_TYPE[32]),
            Comment=''
        )

        instance.PromesaState = constants.PROMESA_STATE[13]
        instance.save()

        return instance


class SendNegociacionINSerializer(serializers.ModelSerializer):
    PromesaState = serializers.CharField(
        read_only=True
    )

    Condition = ConditionSerializer(
        required=False,
        many=True,
        allow_null=True,
        write_only=True
    )

    class Meta:
        model = Promesa
        fields = ('PromesaState', 'Condition')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        conditions_data = validated_data.pop('Condition')

        # Usuarios
        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])
        vendedor_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[2])
        representante_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[0])
        aprobador_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[4])
        # Usuarios
        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=jefe_proyecto_type)
        vendedor_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=vendedor_proyecto_type)
        representante_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=representante_proyecto_type)
        aprobador_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=aprobador_proyecto_type)

        reserva = Reserva.objects.get(Folio=instance.Folio)
        conditions = reserva.ConditionID.all()

        if conditions.exists():
            conditions.delete()

        reserva.ConditionID.clear()
        if conditions_data:
            for condition_data in conditions_data:
                condition = Condition.objects.create(
                    Description=condition_data['Description'],
                    IsImportant=condition_data.get('IsImportant', False),
                    IsApprove=condition_data.get('IsApprove', False)
                )
                reserva.ConditionID.add(condition)
        instance.PromesaState = constants.PROMESA_STATE[14]
        instance.save()

        crear_notificacion_promesa_control_negociacion(instance, instance.ProyectoID, jefe_proyecto, vendedor_proyecto,
                                                       representante_proyecto, aprobador_proyecto)

        VentaLog.objects.create(
            VentaID=instance.PromesaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=VentaLogType.objects.get(
                Name=constants.VENTA_LOG_TYPE[33]),
            Comment=''
        )

        return instance


class ControlNegociacionSerializer(serializers.ModelSerializer):
    PromesaState = serializers.CharField(
        read_only=True
    )

    Condition = ApproveConditionSerializer(
        required=False,
        many=True,
        allow_null=True,
        write_only=True
    )

    Comment = serializers.CharField(
        write_only=True,
        allow_blank=True
    )
    Resolution = serializers.BooleanField(
        write_only=True
    )

    class Meta:
        model = Oferta
        fields = ('Condition', 'PromesaState',
                  'Resolution', 'Comment')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        resolution = validated_data.pop('Resolution')
        conditions_data = validated_data.pop('Condition')
        comment = validated_data.pop('Comment')
        aprobacion_inmobiliaria = instance.AprobacionInmobiliaria
        # Tipos de Usuarios
        vendedor_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[2])

        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])

        # Usuarios
        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=jefe_proyecto_type)

        vendedor = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=vendedor_type)

        if resolution:

            if str(current_user.UserID) in aprobacion_inmobiliaria and aprobacion_inmobiliaria[current_user.UserID]:
                raise CustomValidation(
                    "Aprobada",
                    status_code=status.HTTP_409_CONFLICT)

            aprobacion_inmobiliaria[str(current_user.UserID)] = True;
            instance.AprobacionInmobiliaria = aprobacion_inmobiliaria;

            if (len(aprobacion_inmobiliaria) < UserProyecto.objects.filter(
                    UserProyectoTypeID=UserProyectoType.objects.get(Name='Aprobador'),
                    ProyectoID=instance.ProyectoID).count()):
                instance.save()
                return instance

            for condition_data in conditions_data:
                condition = Condition.objects.get(
                    ConditionID=condition_data['ConditionID'])
                if condition.IsImportant:
                    if not condition_data['IsApprove']:
                        raise CustomValidation(
                            "Revisar todas las condiciones importantes para aprobar promesa",
                            status_code=status.HTTP_409_CONFLICT)
                    condition.IsApprove = True
                    condition.save()

            instance.PromesaState = constants.PROMESA_STATE[1]
            venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[34])
            crear_notificacion_promesa_aprobada_negociacion(instance, jefe_proyecto, vendedor)
        else:
            instance.PromesaState = constants.PROMESA_STATE[15]
            instance.AprobacionInmobiliaria = {};
            venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[35])
            crear_notificacion_promesa_rechazada_negociacion(instance, jefe_proyecto, vendedor)

        VentaLog.objects.create(
            VentaID=instance.PromesaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment,
        )

        instance.save()
        return instance


class ApproveRejectNegociacionSerializer(serializers.ModelSerializer):
    PromesaState = serializers.CharField(
        read_only=True
    )

    Condition = ApproveConditionSerializer(
        required=False,
        many=True,
        allow_null=True,
        write_only=True
    )

    Comment = serializers.CharField(
        write_only=True,
        allow_blank=True
    )
    Resolution = serializers.BooleanField(
        write_only=True
    )

    class Meta:
        model = Oferta
        fields = ('Condition', 'PromesaState',
                  'Resolution', 'Comment')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        resolution = validated_data.pop('Resolution')
        conditions_data = validated_data.pop('Condition')
        comment = validated_data.pop('Comment')

        # Tipos de Usuarios
        vendedor_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[2])

        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])

        # Usuarios
        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=jefe_proyecto_type)

        vendedor = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=vendedor_type)

        if resolution:
            for condition_data in conditions_data:
                condition = Condition.objects.get(
                    ConditionID=condition_data['ConditionID'])
                if condition.IsImportant:
                    if not condition_data['IsApprove']:
                        raise CustomValidation(
                            "Revisar todas las condiciones importantes para aprobar promesa",
                            status_code=status.HTTP_409_CONFLICT)
                    condition.IsApprove = True
                    condition.save()

            instance.PromesaState = constants.PROMESA_STATE[1]
            venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[34])
            crear_notificacion_promesa_aprobada_negociacion(instance, jefe_proyecto, vendedor)
        else:
            instance.PromesaState = constants.PROMESA_STATE[15]
            venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[35])
            crear_notificacion_promesa_rechazada_negociacion(instance, jefe_proyecto, vendedor)

        VentaLog.objects.create(
            VentaID=instance.PromesaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment,
        )

        instance.save()
        return instance
