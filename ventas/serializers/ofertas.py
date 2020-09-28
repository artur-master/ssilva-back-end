from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers, status

from common import constants
from common.notifications import (
    crear_notificacion_oferta_creada,
    crear_notificacion_oferta_pendiente_aprobacion_inmobiliaria,
    crear_notificacion_oferta_aprobada,
    crear_notificacion_oferta_rechazada,
    crear_notificacion_modify_oferta_aprobada,
    crear_notificacion_modify_oferta_rechazada,
    crear_notificacion_pre_aprobacion_aprobada,
    crear_notificacion_pre_aprobacion_rechazada,
    crear_notificacion_oferta_a_confeccion_promesa,
    crear_notificacion_oferta_requiere_aprobacion,
    crear_notificacion_confeccion_promesa_aprobada,
    crear_notificacion_confeccion_promesa_rechazada,
    crear_notificacion_oferta_cancelada,
    crear_notificacion_oferta_modificada,
    crear_notificacion_oferta_refund,
    eliminar_notificacion_oferta_a_confeccion_promesa,
    eliminar_notificacion_oferta_requiere_aprobacion,
    eliminar_notificaciones_oferta)
from common.services import (
    return_current_user, get_or_none)
from common.snippets.graphs.ofertas import return_graph
from common.validations import CustomValidation
from empresas_and_proyectos.models.inmuebles import (
    Inmueble,
    InmuebleState)
from empresas_and_proyectos.models.proyectos import (
    UserProyectoType,
    UserProyecto,
    Proyecto)
from users.models import User, Permission
from users.serializers.users import UserProfileSerializer
from ventas.models.clientes import Cliente
from ventas.models.conditions import Condition
from ventas.models.documents import DocumentVenta
from ventas.models.empresas_compradoras import EmpresaCompradora
from ventas.models.finding_contact import ContactMethodType
from ventas.models.ofertas import Oferta
from ventas.models.patrimonies import Patrimony
from ventas.models.payment_forms import (
    PreAprobacionCredito,
    PayType)
from ventas.models.reservas import (
    Reserva,
    ReservaState,
    ReservaInmueble)
from ventas.models.ventas_logs import (
    VentaLog,
    VentaLogType)
from ventas.serializers import reservas
from ventas.serializers.clientes import ClienteSerializer
from ventas.serializers.conditions import (
    ConditionSerializer,
    ApproveConditionSerializer)
from ventas.serializers.cuotas import ListCuotaSerializer
from ventas.serializers.documents_venta import DocumentVentaSerializer
from ventas.serializers.empresas_compradoras import (
    EmpresaCompradoraSerializer,
    CreateEmpresaCompradoraSerializer)
from ventas.serializers.patrimonies import PatrimonySerializer
from ventas.serializers.promesas import create_promesa
from ventas.serializers.ventas_logs import VentaLogSerializer
from .cuotas import CreateCuotaSerializer
from .reservas import CreateReservaInmuebleSerializer

def get_initAprobacionInmobiliaria(proyecto):
    aprobacionInmobiliaria = {}

    aprobadors = UserProyecto.objects.filter(UserProyectoTypeID=UserProyectoType.objects.get(Name='Aprobador'), ProyectoID=proyecto)
    if aprobadors.exists():
        aprobador_users = {}
        for aprobador in aprobadors:
            aprobador_users[str(aprobador.UserID.UserID)] = None

        aprobacionInmobiliaria['Aprobador'] = aprobador_users

    autorizadors = UserProyecto.objects.filter(UserProyectoTypeID=UserProyectoType.objects.get(Name='Autorizador'), ProyectoID=proyecto)
    if autorizadors.exists():
        autorizador_users = {}
        for autorizador in autorizadors:
            autorizador_users[str(autorizador.UserID.UserID)] = None
            
        aprobacionInmobiliaria['Autorizador'] = autorizador_users
    
    return aprobacionInmobiliaria


def create_oferta(proyecto, cliente, vendedor, codeudor, empresa_compradora, folio, cotizacion_type,
                  contact_method_type, payment_firma_promesa, payment_firma_escritura,
                  payment_institucion_financiera, ahorro_plus,
                  subsidio, subsidio_type, subsidio_certificado, libreta, libreta_number, institucion_financiera,
                  paytype, date_firma_promesa,
                  value_producto_financiero, current_user):
    if paytype.Name == constants.PAY_TYPE[0]:
        pre_aprobacion_credito_state = constants.PRE_APROBACION_CREDITO_STATE[0]
    else:
        pre_aprobacion_credito_state = constants.PRE_APROBACION_CREDITO_STATE[1]

    instance = Oferta.objects.create(
        ProyectoID=proyecto,
        CotizacionTypeID=cotizacion_type,
        ClienteID=cliente,
        VendedorID=vendedor,
        CodeudorID=codeudor,
        EmpresaCompradoraID=empresa_compradora,
        Folio=folio,
        OfertaState=constants.OFERTA_STATE[0],
        AprobacionInmobiliaria=get_initAprobacionInmobiliaria(proyecto),
        AprobacionInmobiliariaState=constants.APROBACION_INMOBILIARIA_STATE[0],
        PreAprobacionCreditoState=pre_aprobacion_credito_state,
        RecepcionGarantiaState=constants.RECEPCION_GARANTIA_STATE[0],
        ContactMethodTypeID=contact_method_type,
        PaymentFirmaPromesa=payment_firma_promesa,
        PaymentFirmaEscritura=payment_firma_escritura,
        PaymentInstitucionFinanciera=payment_institucion_financiera,
        AhorroPlus=ahorro_plus,
        Subsidio=subsidio,
        SubsidioType=subsidio_type,
        SubsidioCertificado=subsidio_certificado,
        Libreta=libreta,
        LibretaNumber=libreta_number,
        InstitucionFinancieraID=institucion_financiera,
        PayTypeID=paytype,
        DateFirmaPromesa=date_firma_promesa,
        ValueProductoFinanciero=value_producto_financiero,
    )

    venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[6])

    comment = "Creacion: Oferta {0} proyecto {1}".format(instance.Folio, proyecto.Name)

    VentaLog.objects.create(
        VentaID=instance.OfertaID,
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

    asistente_comercial_type = UserProyectoType.objects.get(
        Name=constants.USER_PROYECTO_TYPE[3])

    # Usuarios
    jefe_proyecto = UserProyecto.objects.filter(
        ProyectoID=proyecto,
        UserProyectoTypeID=jefe_proyecto_type)

    vendedor = UserProyecto.objects.filter(
        ProyectoID=proyecto,
        UserProyectoTypeID=vendedor_type)

    asistente_comercial = UserProyecto.objects.filter(
        ProyectoID=proyecto,
        UserProyectoTypeID=asistente_comercial_type)

    permission = Permission.objects.get(Name=constants.PERMISSIONS[20])

    usuarios_recepciona_garantias = User.objects.filter(
        RoleID__PermissionID=permission
    )
    crear_notificacion_oferta_creada(
        instance, proyecto, jefe_proyecto, vendedor,
        asistente_comercial, usuarios_recepciona_garantias)
    
    return instance


class SendApproveInmobiliariaSerializer(serializers.ModelSerializer):
    Conditions = ConditionSerializer(
        required=False,
        many=True,
        allow_null=True,
        write_only=True
    )
    AprobacionInmobiliariaState = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Oferta
        fields = ('Conditions', 'AprobacionInmobiliariaState')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        conditions_data = validated_data.pop('Conditions')
        reserva = Reserva.objects.get(Folio=instance.Folio)
        conditions = reserva.ConditionID.all()

        if instance.IsApproveInmobiliaria:
            instance.AprobacionInmobiliariaState = constants.APROBACION_INMOBILIARIA_STATE[2]
            instance.save()
            raise CustomValidation(
                "Oferta ya tenia aprobación por parte de la inmobiliaria",
                status_code=status.HTTP_409_CONFLICT)

        if conditions.exists():
            conditions.delete()

        reserva.ConditionID.clear()
        if conditions_data:
            for condition_data in conditions_data:
                condition = Condition.objects.create(
                    Description=condition_data['Description'],
                    IsImportant=condition_data.get('IsImportant', False)
                )
                reserva.ConditionID.add(condition)

        if "Autorizador" in instance.AprobacionInmobiliaria:
            instance.AprobacionInmobiliariaState = constants.APROBACION_INMOBILIARIA_STATE[4]
        else:
            instance.AprobacionInmobiliariaState = constants.APROBACION_INMOBILIARIA_STATE[1]

        instance.save()

        venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[7])
        comment = "Oferta {0} proyecto {1} enviada a aprobacion".format(instance.Folio, instance.ProyectoID)

        VentaLog.objects.create(
            VentaID=instance.OfertaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment,
        )

        # Crear notificaciones y  Envio de correo
        # Tipos de Usuarios
        recipients = list()
        representante_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[0])

        aprobador_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[4])

        # Usuarios
        representantes = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=representante_type)

        aprobadores = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=aprobador_type)

        crear_notificacion_oferta_pendiente_aprobacion_inmobiliaria(
            instance, representantes, aprobadores)

        for representante in representantes:
            recipients.append(representante.UserID)

        for aprobador in aprobadores:
            recipients.append(aprobador.UserID)

        subject = "Oferta {0} proyecto {1}, requiere aprobación".format(instance.Folio, instance.ProyectoID)
        extra_data = {
            'folio': instance.Folio,
            'name': instance.ProyectoID
        }
        # send_email_to_inmobiliaria(subject, 'oferta_approve.html', recipients, extra_data)

        return instance


class ApproveInmobiliariaSerializer(serializers.ModelSerializer):
    Conditions = ApproveConditionSerializer(
        required=False,
        many=True,
        allow_null=True,
        write_only=True
    )
    AprobacionInmobiliariaState = serializers.CharField(
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
        model = Oferta
        fields = ('Conditions', 'AprobacionInmobiliariaState',
                  'Resolution', 'Comment')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        role = self.context['request'].data['Role']

        resolution = validated_data.pop('Resolution')
        conditions_data = validated_data.pop('Conditions')
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
            if instance.AprobacionInmobiliariaState == constants.APROBACION_INMOBILIARIA_STATE[2]:
                raise CustomValidation(
                    "Oferta ya esta aprobada",
                    status_code=status.HTTP_409_CONFLICT)

            if role in aprobacion_inmobiliaria and aprobacion_inmobiliaria[role][str(current_user.UserID)]:
                raise CustomValidation(
                    "Aprobada",
                    status_code=status.HTTP_409_CONFLICT)

            aprobacion_inmobiliaria[role][str(current_user.UserID)] = True
            instance.AprobacionInmobiliaria = aprobacion_inmobiliaria
            venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[8])
            
            # if (len(aprobacion_inmobiliaria) < UserProyecto.objects.filter(
            #         UserProyectoTypeID=UserProyectoType.objects.get(Name='Aprobador'),
            #         ProyectoID=instance.ProyectoID).count()):
            #     VentaLog.objects.create(
            #         VentaID=instance.OfertaID,
            #         Folio=instance.Folio,
            #         UserID=current_user,
            #         ClienteID=instance.ClienteID,
            #         ProyectoID=instance.ProyectoID,
            #         VentaLogTypeID=venta_log_type,
            #         Comment='',
            #     )
            #     instance.save()
            #     return instance

            for condition_data in conditions_data:
                condition = Condition.objects.get(
                    ConditionID=condition_data['ConditionID'])
                if condition.IsImportant:
                    if not condition_data['IsApprove']:
                        raise CustomValidation(
                            "Revisar todas las condiciones importantes para aprobar oferta",
                            status_code=status.HTTP_409_CONFLICT)
                    condition.IsApprove = True
                    condition.save()

            if role == 'Autorizador':
                instance.AprobacionInmobiliariaState = constants.APROBACION_INMOBILIARIA_STATE[6]
            else:
                isApprova = True
                for user_role in aprobacion_inmobiliaria.keys():
                    for value in aprobacion_inmobiliaria[user_role].values():
                        if value == None:
                            isApprova = False
                if isApprova:
                    instance.AprobacionInmobiliariaState = constants.APROBACION_INMOBILIARIA_STATE[2]
                    instance.IsApproveInmobiliaria = True

            crear_notificacion_oferta_aprobada(instance, jefe_proyecto, vendedor)
        else:
            instance.AprobacionInmobiliariaState = constants.APROBACION_INMOBILIARIA_STATE[3]
            aprobacion_inmobiliaria[role][str(current_user.UserID)] = False
            instance.AprobacionInmobiliaria = aprobacion_inmobiliaria
            venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[9])

            crear_notificacion_oferta_rechazada(instance, jefe_proyecto, vendedor)

        VentaLog.objects.create(
            VentaID=instance.OfertaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment,
            CommentBySystem=False
        )

        send_to_confeccion_promesa(instance, current_user)
        instance.save()
        return instance


class RetrieveOfertaSerializer(serializers.ModelSerializer):
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )
    Proyecto = serializers.CharField(
        source='ProyectoID.Name'
    )
    EmpresaCompradora = EmpresaCompradoraSerializer(
        source='EmpresaCompradoraID',
        allow_null=True
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
    PayTypeID = serializers.UUIDField(
        source='PayTypeID.PayTypeID',
        allow_null=True
    )
    PayType = serializers.CharField(
        source='PayTypeID.Name'
    )
    ContactMethodTypeID = serializers.UUIDField(
        source='ContactMethodTypeID.ContactMethodTypeID',
        allow_null=True
    )
    ContactMethodType = serializers.CharField(
        source='ContactMethodTypeID.Name'
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
    ValueProductoFinanciero = serializers.DecimalField(
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
    Condition = serializers.SerializerMethodField('get_conditions')
    Cuotas = serializers.SerializerMethodField('get_cuotas')
    Inmuebles = serializers.SerializerMethodField('get_inmuebles')
    Documents = serializers.SerializerMethodField('get_documents')
    IsFinished = serializers.SerializerMethodField('get_state_oferta')
    Graph = serializers.SerializerMethodField('get_graph')
    Patrimony = serializers.SerializerMethodField('get_patrimony')
    Date = serializers.SerializerMethodField('get_date')
    Logs = serializers.SerializerMethodField('get_logs')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ProyectoID',
            'ClienteID',
            'VendedorID',
            'CodeudorID',
            'PayTypeID',
            'ContactMethodTypeID',
            'EmpresaCompradoraID')
        return queryset

    class Meta:
        model = Oferta
        fields = (
            'OfertaID',
            'ProyectoID',
            'Proyecto',
            'CotizacionType',
            'ClienteID',
            'Cliente',
            'Date',
            'EmpresaCompradora',
            'VendedorID',
            'Vendedor',
            'CodeudorID',
            'Codeudor',
            'Folio',
            'OfertaState',
            'AprobacionInmobiliariaState',
            'AprobacionInmobiliaria',
            'PreAprobacionCreditoState',
            'RecepcionGarantiaState',
            'PayTypeID',
            'PayType',
            'ContactMethodTypeID',
            'ContactMethodType',
            'DateFirmaPromesa',
            'PaymentFirmaPromesa',
            'PaymentFirmaEscritura',
            'PaymentInstitucionFinanciera',
            'ValueProductoFinanciero',
            'AhorroPlus',
            'Subsidio',
            'SubsidioType',
            'SubsidioCertificado',
            'Libreta',
            'LibretaNumber',
            'InstitucionFinancieraID',
            'Condition',
            'Cuotas',
            'Inmuebles',
            'Documents',
            'IsFinished',
            'Graph',
            'Patrimony',
            'Logs'
        )

    def get_patrimony(self, obj):
        try:
            reserva = Reserva.objects.filter(Folio=obj.Folio).first()
            patrimonies = Patrimony.objects.filter(ClienteID=reserva.ClienteID)

            return PatrimonySerializer(instance=patrimonies[0]).data
        except:
            return None

    def get_conditions(self, obj):
        reserva = Reserva.objects.filter(Folio=obj.Folio).first()
        try:
            conditions = reserva.ConditionID.all()
            serializer = ConditionSerializer(
                instance=conditions, many=True)
            return serializer.data
        except:
            return None

    def get_cuotas(self, obj):
        try:
            reserva = Reserva.objects.filter(Folio=obj.Folio).first()
            cuotas = reserva.CuotaID.all()
            serializer = ListCuotaSerializer(
                instance=cuotas, many=True)
            return serializer.data
        except:
            return None

    def get_inmuebles(self, obj):
        reserva = Reserva.objects.filter(Folio=obj.Folio).first()
        inmuebles_reserva = ReservaInmueble.objects.filter(
            ReservaID=reserva)
        serializer = reservas.ListReservaInmuebleSerializer(
            instance=inmuebles_reserva, context={'url': self.context['request']}, many=True)
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

    def get_graph(self, obj):
        graph = return_graph(obj)
        if obj.OfertaState == constants.OFERTA_STATE[3]:
            return {}
        else:
            return graph

    def get_state_oferta(self, obj):
        if obj.OfertaState == constants.OFERTA_STATE[3]:
            return True
        else:
            return False

    def get_date(self, obj):
        try:
            return obj.Date.strftime("%Y-%m-%d")
        except AttributeError:
            return ""

    def get_logs(self, obj):
        venta_log = VentaLog.objects.filter(
            # VentaLogTypeID__in=VentaLogType.objects.filter(Name__in=constants.VENTA_LOG_TYPE),
            Folio=obj.Folio).order_by('-id')
        serializer = VentaLogSerializer(instance=venta_log, many=True)
        return serializer.data


class ListInmuebleOfertaSerializer(serializers.ModelSerializer):
    InmuebleID = serializers.CharField(
        source='InmuebleID.InmuebleID'
    )
    InmuebleType = serializers.CharField(
        source='InmuebleID.InmuebleTypeID.Name'
    )
    Number = serializers.CharField(
        source='InmuebleID.Number'
    )

    class Meta:
        model = ReservaInmueble
        fields = ('InmuebleID', 'InmuebleType', 'Number')


class ListOfertaSerializer(serializers.ModelSerializer):
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )
    Proyecto = serializers.CharField(
        source='ProyectoID.Name'
    )
    Cliente = ClienteSerializer(
        source='ClienteID',
        allow_null=True
    )
    '''
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
    '''
    Inmuebles = serializers.SerializerMethodField('get_inmuebles')
    PromesaID = serializers.SerializerMethodField('get_promesa_id')
    PayType = serializers.CharField(
        source='PayTypeID.Name'
    )

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ProyectoID', 'ClienteID')
        return queryset

    class Meta:
        model = Oferta
        fields = ('OfertaID', 'ProyectoID', 'Proyecto', 'Date', 'Folio', 'Cliente',
                  #'ClienteID', 'ClienteName', 'ClienteLastNames', 'ClienteRut', 
                  'AprobacionInmobiliaria', 'AprobacionInmobiliariaState','PayType',
                  'OfertaState', 'RecepcionGarantiaState', 'Inmuebles', 'PromesaID')

    def get_inmuebles(self, obj):
        reserva = Reserva.objects.filter(Folio=obj.Folio).first()
        inmuebles_reserva = ReservaInmueble.objects.filter(
            ReservaID=reserva)
        serializer = ListInmuebleOfertaSerializer(
            instance=inmuebles_reserva, many=True)
        return serializer.data
    
    def get_promesa_id(self, obj):
        try:
            return obj.PromesaID.PromesaID
        except AttributeError:
            return None


class RegisterReceptionGuaranteeSerializer(serializers.ModelSerializer):
    RecepcionGarantiaState = serializers.CharField(
        read_only=True
    )
    Refund = serializers.BooleanField(
        write_only=True
    )

    class Meta:
        model = Oferta
        fields = ('RecepcionGarantiaState', 'Refund')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        refund = validated_data.pop('Refund')

        if refund:
            if instance.RecepcionGarantiaState != constants.RECEPCION_GARANTIA_STATE[1]:
                raise CustomValidation(
                    "No Recepcion de garantia",
                    status_code=status.HTTP_409_CONFLICT)
            instance.RecepcionGarantiaState = constants.RECEPCION_GARANTIA_STATE[2]
            venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[31])
            comment = "Oferta {0} garantia refund".format(instance.Folio)

        else:
            if instance.RecepcionGarantiaState == constants.RECEPCION_GARANTIA_STATE[1]:
                raise CustomValidation(
                    "Recepcion de garantia ya ha sido ingresada",
                    status_code=status.HTTP_409_CONFLICT)

            instance.RecepcionGarantiaState = constants.RECEPCION_GARANTIA_STATE[1]

            venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[10])

            comment = "Oferta {0} garantia recepcionada".format(instance.Folio)

        VentaLog.objects.create(
            VentaID=instance.OfertaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment,
        )

        send_to_confeccion_promesa(instance, current_user)
        instance.save()
        return instance


class RegisterInstitucionFinancieraSerializer(serializers.ModelSerializer):
    InstitucionFinanciera = serializers.CharField(
    )
    OfertaID = serializers.CharField(
        write_only=True
    )
    Date = serializers.DateTimeField(
        allow_null=True,
        required=False,
    )
    Observacion = serializers.CharField(
        allow_null=True,
        allow_blank=True,
        required=False
    )
    DocumentCredit = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentPreApprobal = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    Result = serializers.CharField(
        allow_null=True,
        required=False
    )

    class Meta:
        model = PreAprobacionCredito
        fields = (
            'PreAprobacionCreditoID', 'InstitucionFinanciera', 
            'OfertaID', 'Date', 'Observacion',
            'DocumentCredit', 'DocumentPreApprobal',
            'Result')

    def create(self, validated_data):
        oferta_id = validated_data['OfertaID']
        oferta = Oferta.objects.get(OfertaID=oferta_id)

        instance = PreAprobacionCredito.objects.create(
            Date=validated_data.get('Date', None),
            OfertaID=oferta,
            InstitucionFinanciera=validated_data['InstitucionFinanciera'],
            Observacion=validated_data.get('Observacion', ''),
            DocumentCredit=validated_data.get('DocumentCredit', ''),
            DocumentPreApprobal=validated_data.get('DocumentPreApprobal', ''),
            Result=validated_data.get('Result', '')
        )

        return instance


class ListPreAprobacionCreditoSerializer(serializers.ModelSerializer):
    Date = serializers.SerializerMethodField('get_date')
    DocumentCredit = serializers.SerializerMethodField('get_documentCredit')
    DocumentPreApprobal = serializers.SerializerMethodField('get_documentPreApprobal')
    
    class Meta:
        model = PreAprobacionCredito
        fields = ('PreAprobacionCreditoID', 'InstitucionFinanciera',
                  'Date', 'Result', 'Observacion', 'DocumentCredit', 'DocumentPreApprobal')

    def get_date(self, obj):
        try:
            return obj.Date.strftime("%Y-%m-%d")
        except AttributeError:
            return ""

    def get_documentCredit(self, obj):
        if obj.DocumentCredit:
            return "http://" + get_current_site(self.context.get('request')).domain + obj.DocumentCredit.url
        else:
            return ""

    def get_documentPreApprobal(self, obj):
        if obj.DocumentPreApprobal:
            return "http://" + get_current_site(self.context.get('request')).domain + obj.DocumentPreApprobal.url
        else:
            return ""


class RegisterResultPreAprobacionSerializer(serializers.ModelSerializer):
    PreAprobacionCreditoID = serializers.CharField(
        write_only=True
    )
    Result = serializers.CharField(
        write_only=True
    )
    PreAprobacionCreditoState = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Oferta
        fields = ('PreAprobacionCreditoID', 'Result',
                  'PreAprobacionCreditoState')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        pre_aprobacion_credito_id = validated_data['PreAprobacionCreditoID']
        result = validated_data['Result']
        pre_aprobacion_credito = PreAprobacionCredito.objects.get(
            PreAprobacionCreditoID=pre_aprobacion_credito_id)

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

        if result == constants.RESULT[0]:
            pre_aprobacion_credito.Result = constants.RESULT[0]
            instance.PreAprobacionCreditoState = constants.PRE_APROBACION_CREDITO_STATE[2]
            crear_notificacion_pre_aprobacion_aprobada(instance, jefe_proyecto, vendedor)
        else:
            PreAprobacionCredito.objects.filter(OfertaID=instance.OfertaID).update(Result=constants.RESULT[1])
            pre_aprobacion_credito.Result = constants.RESULT[1]
            instance.PreAprobacionCreditoState = constants.PRE_APROBACION_CREDITO_STATE[3]
            crear_notificacion_pre_aprobacion_rechazada(instance, jefe_proyecto, vendedor)

        send_to_confeccion_promesa(instance, current_user)
        pre_aprobacion_credito.save()
        instance.save()

        return instance


def send_to_confeccion_promesa(oferta, current_user):
    # Tipos de Usuarios
    vendedor_type = UserProyectoType.objects.get(
        Name=constants.USER_PROYECTO_TYPE[2])

    jefe_proyecto_type = UserProyectoType.objects.get(
        Name=constants.USER_PROYECTO_TYPE[1])

    # Usuarios
    jefe_proyecto = UserProyecto.objects.filter(
        ProyectoID=oferta.ProyectoID,
        UserProyectoTypeID=jefe_proyecto_type)

    vendedor = UserProyecto.objects.filter(
        ProyectoID=oferta.ProyectoID,
        UserProyectoTypeID=vendedor_type)

    permission = Permission.objects.get(Name=constants.PERMISSIONS[21])

    usuarios_aprueba_confeccion_promesa = User.objects.filter(
        RoleID__PermissionID=permission
    )

    if (oferta.AprobacionInmobiliariaState == constants.APROBACION_INMOBILIARIA_STATE[2] and
            (oferta.PreAprobacionCreditoState == constants.PRE_APROBACION_CREDITO_STATE[2] or
             oferta.PreAprobacionCreditoState == constants.PRE_APROBACION_CREDITO_STATE[0]) and
            oferta.RecepcionGarantiaState == constants.RECEPCION_GARANTIA_STATE[1] and
            oferta.OfertaState != constants.OFERTA_STATE[5]):
        oferta.OfertaState = constants.OFERTA_STATE[1]

        venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[11])
        comment = "Envio oferta {} a confeccion de promesa".format(oferta.Folio)

        VentaLog.objects.create(
            VentaID=oferta.OfertaID,
            Folio=oferta.Folio,
            UserID=current_user,
            ClienteID=oferta.ClienteID,
            ProyectoID=oferta.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment,
        )

        crear_notificacion_oferta_a_confeccion_promesa(
            oferta, jefe_proyecto, vendedor)

        crear_notificacion_oferta_requiere_aprobacion(
            oferta, usuarios_aprueba_confeccion_promesa
        )

    if oferta.OfertaState == constants.OFERTA_STATE[5] and oferta.RecepcionGarantiaState == \
            constants.RECEPCION_GARANTIA_STATE[2]:
        crear_notificacion_oferta_refund(oferta, jefe_proyecto, vendedor)


class ApproveConfeccionPromesaSerializer(serializers.ModelSerializer):
    OfertaState = serializers.CharField(
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
        model = Oferta
        fields = ('OfertaState', 'Resolution', 'Comment')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        resolution = validated_data.pop('Resolution')
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
            if instance.OfertaState == constants.OFERTA_STATE[3]:
                raise CustomValidation(
                    "Confeccion de promesa ya ha sido aprobada",
                    status_code=status.HTTP_409_CONFLICT)

            instance.OfertaState = constants.OFERTA_STATE[3]
            venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[12])

            crear_notificacion_confeccion_promesa_aprobada(instance, jefe_proyecto, vendedor)

            # Create promesa
            reserva = Reserva.objects.get(Folio=instance.Folio)
            inmuebles = ReservaInmueble.objects.filter(ReservaID=reserva)

            instance.PromesaID = create_promesa(instance.ProyectoID, instance.ClienteID, instance.VendedorID, instance.CodeudorID,
                           inmuebles, instance.Folio, instance.CotizacionTypeID, instance.PaymentFirmaPromesa,
                           instance.PaymentFirmaEscritura,
                           instance.PaymentInstitucionFinanciera, instance.AhorroPlus, instance.PayTypeID, current_user)
        else:
            if instance.OfertaState == constants.OFERTA_STATE[3]:
                raise CustomValidation(
                    "Confeccion de promesa ya ha sido aprobada, no se puede rechazar",
                    status_code=status.HTTP_409_CONFLICT)
            instance.OfertaState = constants.OFERTA_STATE[2]

            if instance.PromesaID:
                instance.PromesaID.delete()            
            instance.PromesaID = None

            # reset oferta
            if instance.PayTypeID.Name == constants.PAY_TYPE[0]:
                instance.PreAprobacionCreditoState = constants.PRE_APROBACION_CREDITO_STATE[0]
            else:
                instance.PreAprobacionCreditoState = constants.PRE_APROBACION_CREDITO_STATE[1]
            instance.AprobacionInmobiliariaState = constants.APROBACION_INMOBILIARIA_STATE[0]
            instance.RecepcionGarantiaState = constants.RECEPCION_GARANTIA_STATE[0]

            venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[13])

            crear_notificacion_confeccion_promesa_rechazada(instance, jefe_proyecto, vendedor)

        eliminar_notificacion_oferta_a_confeccion_promesa(instance)
        eliminar_notificacion_oferta_requiere_aprobacion(instance)

        VentaLog.objects.create(
            VentaID=instance.OfertaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment,
            CommentBySystem=False
        )

        instance.save()

        return instance


class ApproveUpdateOfertaSerializer(serializers.ModelSerializer):
    OfertaState = serializers.CharField(
        read_only=True
    )
    Resolution = serializers.BooleanField(
        write_only=True
    )

    class Meta:
        model = Oferta
        fields = ('OfertaState', 'Resolution')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        resolution = validated_data.pop('Resolution')

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
            instance.OfertaState = constants.OFERTA_STATE[0]
            venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[29])
            crear_notificacion_modify_oferta_aprobada(instance, jefe_proyecto, vendedor)
        else:
            instance.OfertaState = constants.OFERTA_STATE[2]
            venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[28])
            crear_notificacion_modify_oferta_rechazada(instance, jefe_proyecto, vendedor)

        VentaLog.objects.create(
            VentaID=instance.OfertaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
        )

        instance.save()

        return instance


class CancelOfertaSerializer(serializers.ModelSerializer):
    OfertaState = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Reserva
        fields = ('OfertaState',)

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        if instance.OfertaState == constants.OFERTA_STATE[4]:
            raise CustomValidation(
                "Oferta ya está cancelada",
                status_code=status.HTTP_409_CONFLICT)

        if instance.OfertaState == constants.OFERTA_STATE[3]:
            raise CustomValidation(
                "Oferta en estado promesa no se puede cancelar",
                status_code=status.HTTP_409_CONFLICT)

        # Registro en historial de ventas
        venta_log_type = VentaLogType.objects.get(
            Name=constants.VENTA_LOG_TYPE[14])

        VentaLog.objects.create(
            VentaID=instance.OfertaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type
        )

        # Volver inmuebles asociados a estado disponible
        reserva = Reserva.objects.get(Folio=instance.Folio)
        reserva_inmuebles = ReservaInmueble.objects.filter(ReservaID=reserva)
        inmueble_state = InmuebleState.objects.get(
            Name=constants.INMUEBLE_STATE[0])

        for reserva_inmueble in reserva_inmuebles:
            inmueble = reserva_inmueble.InmuebleID
            inmueble.InmuebleStateID = inmueble_state
            inmueble.save()

        # Crear/Eliminar notificaciones
        # Tipos de Usuarios
        vendedor_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[2])

        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])

        asistente_comercial_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[3])

        representante_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[0])

        aprobador_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[4])

        # Usuarios
        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=jefe_proyecto_type)

        vendedor = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID, UserProyectoTypeID=vendedor_type)

        asistente_comercial = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=asistente_comercial_type)

        representantes = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=representante_type)

        aprobadores = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=aprobador_type)

        eliminar_notificaciones_oferta(instance)

        if (instance.AprobacionInmobiliariaState == constants.APROBACION_INMOBILIARIA_STATE[0] or
                instance.AprobacionInmobiliariaState == constants.APROBACION_INMOBILIARIA_STATE[1]):
            crear_notificacion_oferta_cancelada(
                instance, jefe_proyecto, vendedor, asistente_comercial, representantes, aprobadores)
        else:
            crear_notificacion_oferta_cancelada(
                instance, jefe_proyecto, vendedor, asistente_comercial, representantes, aprobadores)

        instance.OfertaState = constants.OFERTA_STATE[4]
        instance.save()

        return instance


class UpdateOfertaSerializer(serializers.ModelSerializer):
    EmpresaCompradora = CreateEmpresaCompradoraSerializer(
        source='EmpresaCompradoraID',
        allow_null=True,
        required=False
    )
    ProyectoID = serializers.UUIDField(
        write_only=True
    )
    ClienteID = serializers.UUIDField(
        write_only=True
    )
    CodeudorID = serializers.UUIDField(
        write_only=True,
        allow_null=True
    )
    PayTypeID = serializers.UUIDField(
        write_only=True
    )
    ContactMethodTypeID = serializers.UUIDField(
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
    Subsidio = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True,
        required=False
    )
    Libreta = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True,
        required=False
    )
    DateFirmaPromesa = serializers.DateTimeField(
        write_only=True,
        allow_null=True
    )
    ValueProductoFinanciero = serializers.IntegerField(
        write_only=True
    )
    Cuotas = CreateCuotaSerializer(
        source='CuotaID',
        many=True,
        required=False
    )
    Inmuebles = CreateReservaInmuebleSerializer(
        source='InmuebleID',
        many=True,
        required=False
    )
    Comment = serializers.CharField(
        write_only=True,
        required=False
    )

    class Meta:
        model = Oferta
        fields = (
            'ProyectoID',
            'ClienteID',
            'CodeudorID',
            'PayTypeID',
            'EmpresaCompradora',
            'ContactMethodTypeID',
            'PaymentFirmaPromesa',
            'PaymentFirmaEscritura',
            'PaymentInstitucionFinanciera',
            'AhorroPlus',
            'Subsidio',
            'SubsidioType',
            'SubsidioCertificado',
            'Libreta',
            'LibretaNumber',
            'InstitucionFinancieraID',
            'DateFirmaPromesa',
            'ValueProductoFinanciero',
            'Cuotas',
            'Inmuebles',
            'Comment',
        )

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        if instance.OfertaState == constants.OFERTA_STATE[3]:
            raise CustomValidation(
                "Oferta en estado promesa, debe modificar promesa",
                status_code=status.HTTP_409_CONFLICT)

        proyecto_id = validated_data['ProyectoID']
        cliente_id = validated_data['ClienteID']
        codeudor_id = validated_data['CodeudorID']
        pay_type_id = validated_data['PayTypeID']
        contact_method_type_id = validated_data['ContactMethodTypeID']
        date_firma_promesa = validated_data['DateFirmaPromesa']
        value_producto_financiero = validated_data['ValueProductoFinanciero']

        empresa_compradora_data = validated_data.pop('EmpresaCompradoraID')
        if empresa_compradora_data:
            razon_social_empresa_compradora = empresa_compradora_data['RazonSocial']
            rut_empresa_compradora = empresa_compradora_data['Rut']
            direccion_empresa_compradora = empresa_compradora_data['Address']

        pay_type = get_or_none(PayType, PayTypeID=pay_type_id)
        # Validaciones campos obligatorios
        if not pay_type:
            raise CustomValidation(
                "Debe ingresar tipo de pago",
                status_code=status.HTTP_409_CONFLICT)

        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        cliente = Cliente.objects.get(UserID=cliente_id)
        contact_method_type = ContactMethodType.objects.get(
            ContactMethodTypeID=contact_method_type_id)

        if codeudor_id:
            codeudor = Cliente.objects.get(UserID=codeudor_id)
        else:
            codeudor = None

        if empresa_compradora_data:
            empresa_compradora = EmpresaCompradora.objects.get(
                ClienteID=cliente
            )
            empresa_compradora.RazonSocial = razon_social_empresa_compradora
            empresa_compradora.Rut = rut_empresa_compradora
            empresa_compradora.Address = direccion_empresa_compradora
            empresa_compradora.save()
        else:
            empresa_compradora = None

        instance.ClienteID = cliente
        instance.VendedorID = current_user
        instance.CodeudorID = codeudor
        instance.ContactMethodTypeID = contact_method_type
        instance.EmpresaCompradoraID = empresa_compradora

        # Modificado state
        instance.OfertaState = constants.OFERTA_STATE[5]
        instance.AprobacionInmobiliariaState = constants.APROBACION_INMOBILIARIA_STATE[0]
        instance.RecepcionGarantiaState = constants.RECEPCION_GARANTIA_STATE[0]
        instance.PaymentFirmaPromesa = validated_data['PaymentFirmaPromesa']
        instance.PaymentFirmaEscritura = validated_data['PaymentFirmaEscritura']
        instance.PaymentInstitucionFinanciera = validated_data['PaymentInstitucionFinanciera']
        if 'AhorroPlus' in validated_data:
            instance.AhorroPlus = validated_data['AhorroPlus']
        if 'Subsidio' in validated_data:
            instance.Subsidio = validated_data['Subsidio']
        if 'SubsidioType' in validated_data:
            instance.SubsidioType = validated_data['SubsidioType']
        if 'SubsidioCertificado' in validated_data:
            instance.SubsidioCertificado = validated_data['SubsidioCertificado']
        if 'Libreta' in validated_data:
            instance.Libreta = validated_data['Libreta']
        if 'LibretaNumber' in validated_data:
            instance.LibretaNumber = validated_data['LibretaNumber']
        if 'InstitucionFinancieraID' in validated_data:
            instance.InstitucionFinancieraID = validated_data['InstitucionFinancieraID']
        instance.PayTypeID = pay_type
        instance.DateFirmaPromesa = date_firma_promesa
        instance.ValueProductoFinanciero = value_producto_financiero
        instance.IsApproveInmobiliaria = False
        instance.AprobacionInmobiliaria = {}
        # if pay_type.Name == constants.PAY_TYPE[0] or empresa_compradora:
        if pay_type.Name == constants.PAY_TYPE[0]:
            instance.PreAprobacionCreditoState = constants.PRE_APROBACION_CREDITO_STATE[0]
        else:
            instance.PreAprobacionCreditoState = constants.PRE_APROBACION_CREDITO_STATE[1]

        reserva = Reserva.objects.get(Folio=instance.Folio)

        reserva_state = ReservaState.objects.get(Name=constants.RESERVA_STATE[1])
        reserva.ReservaStateID = reserva_state
        # reserva datas has to be changed. Artur 
        reserva.save()

        # inmuebles update        
        inmuebles_data = validated_data.get('InmuebleID', [])
        
        reserva_inmuebles = list()

        for inmueble_data in inmuebles_data:
            inmueble = Inmueble.objects.get(
                InmuebleID=inmueble_data['InmuebleID']
            )
            inmueble_state = InmuebleState.objects.get(
                Name=constants.INMUEBLE_STATE[2]
            )

            inmueble.InmuebleStateID = inmueble_state
            inmueble.save()

            if inmueble_data['Discount']:
                discount = inmueble_data['Discount']
            else:
                discount = 0

            reserva_inmuebles_qs = ReservaInmueble.objects.filter(
                ReservaID=reserva)

            if reserva_inmuebles_qs.exists():
                reserva_inmuebles_qs.delete()

            reserva_inmueble = ReservaInmueble()
            reserva_inmueble.ReservaID = reserva
            reserva_inmueble.InmuebleID = inmueble
            reserva_inmueble.Discount = discount

            reserva_inmuebles.append(reserva_inmueble)

        ReservaInmueble.objects.bulk_create(reserva_inmuebles)

        # Crear notificaciones
        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])
        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=jefe_proyecto_type)

        vendedor_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[2])
        vendedor = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=vendedor_type)

        asistente_comercial_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[3])
        asistente_comercial = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=asistente_comercial_type)

        crear_notificacion_oferta_modificada(
            instance, jefe_proyecto, vendedor, asistente_comercial)

        # Registro Bitacora de Ventas
        venta_log_type = VentaLogType.objects.get(
            Name=constants.VENTA_LOG_TYPE[15])

        VentaLog.objects.create(
            VentaID=instance.OfertaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=cliente,
            ProyectoID=proyecto,
            VentaLogTypeID=venta_log_type,
            Comment=validated_data['Comment'],
            CommentBySystem=False
        )

        instance.save()

        return instance


class ListOfertaActionSerializer(serializers.ModelSerializer):

    ApprovedUserInfo = serializers.SerializerMethodField('get_user')
    Date = serializers.SerializerMethodField('get_date')
    SaleState = serializers.SerializerMethodField('get_state')
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )
    VentaID = serializers.CharField(
        source='OfertaID'
    )

    class Meta:
        model = Oferta
        fields = ('OfertaID', 'Folio', 'OfertaState', 'ProyectoID',
                  'Date', 'ApprovedUserInfo', 'SaleState', 'VentaID')

    def get_user(self, obj):
        venta_log = VentaLog.objects.filter(VentaID=obj.OfertaID).order_by('-Date').first()
        try:
            user = venta_log.UserID
            UserProFileSerializer = UserProfileSerializer(instance=user)
            return UserProFileSerializer.data
        except:
            return []

    def get_date(self, obj):
        try:
            return obj.Date.strftime("%Y-%m-%d %H:%M")
        except AttributeError:
            return ""

    def get_state(self, obj):
        try:
            return obj.OfertaState+" oferta"
        except AttributeError:
            return ""


class UserOfertaActionSerializer(serializers.ModelSerializer):

    ApprovedUserInfo = serializers.SerializerMethodField('get_user')
    Date = serializers.SerializerMethodField('get_date')
    SaleState = serializers.SerializerMethodField('get_state')
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )

    class Meta:
        model = Oferta
        fields = ('OfertaID', 'Folio', 'OfertaState', 'ProyectoID',
                  'Date', 'ApprovedUserInfo', 'SaleState')

    def get_user(self, obj):
        venta_log = VentaLog.objects.filter(VentaID=obj.OfertaID).order_by('-Date').first()
        if venta_log:
            user = getattr(venta_log, 'UserID')
            UserProFileSerializer = UserProfileSerializer(instance=user)
            return UserProFileSerializer.data
        else:
            return None

    def get_date(self, obj):
        try:
            return obj.Date.strftime("%Y-%m-%d %H:%M")
        except AttributeError:
            return ""

    def get_state(self, obj):
        try:
            return obj.OfertaState + " oferta"
        except AttributeError:
            return ""
