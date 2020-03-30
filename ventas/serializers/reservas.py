import decimal
from django.core.files.base import ContentFile
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status

from common import constants
from common.generate_pdf import (
    render_create_oferta_to_pdf,
    render_create_ficha_to_pdf,
    render_create_simulador_to_pdf)
from common.models import (
    ContactInfoType,
    ConstantNumeric)
from common.notifications import (
    crear_notificacion_reserva_pendiente_informacion,
    crear_notificacion_reserva_pendiente_control,
    crear_notificacion_reserva_rechazada,
    crear_notificacion_reserva_cancelada,
    crear_notificacion_reserva_modificada_pendiente_informacion,
    crear_notificacion_reserva_modificada_pendiente_control,
    eliminar_notificacion_reserva_pendiente_control,
    eliminar_notificacion_reserva_modificada_pendiente_informacion,
    eliminar_notificacion_reserva_informacion_pendiente,
    eliminar_notificacion_reserva_modificada_pendiente_control,
    eliminar_notificaciones_reserva)
from common.services import get_or_none, return_current_user, valor_uf_actual
from common.snippets.graphs.reservas import return_graph
from common.validations import (
    CustomValidation)
from empresas_and_proyectos.models.inmuebles import (
    Inmueble,
    InmuebleState)
from empresas_and_proyectos.models.inmuebles_restrictions import InmuebleInmueble
from empresas_and_proyectos.models.proyectos import (
    Proyecto,
    UserProyecto,
    UserProyectoType)
from empresas_and_proyectos.serializers.inmuebles import ListOrientationSerializer
from empresas_and_proyectos.serializers.proyectos import RestrictionSerializer
from users.serializers.users import UserProfileSerializer
from ventas.models.clientes import (
    Cliente,
    ClienteContactInfo)
from ventas.models.conditions import Condition
from ventas.models.cotizaciones import (
    Cotizacion,
    CotizacionState)
from ventas.models.counter_folios import CounterFolio
from ventas.models.documents import DocumentVenta
from ventas.models.empleadores import Empleador
from ventas.models.empresas_compradoras import EmpresaCompradora
from ventas.models.finding_contact import ContactMethodType
from ventas.models.patrimonies import Patrimony
from ventas.models.payment_forms import (
    PayType,
    Cuota)
from ventas.models.reservas import (
    Reserva,
    ReservaInmueble,
    ReservaState)
from ventas.models.ventas_logs import (
    VentaLogType,
    VentaLog)
from ventas.serializers import ofertas
from ventas.serializers.clientes import ClienteSerializer
from ventas.serializers.cotizaciones import (CreateClienteCotizacionSerializer, CotizacionType)
from ventas.serializers.documents_venta import DocumentVentaSerializer
from ventas.serializers.patrimonies import PatrimonySerializer
from ventas.snippets.clientes_serializers import save_cliente_return
from ventas.snippets.utils import (
    calculate_totals_patrimony,
    calculate_simulate_values)
from .conditions import (
    ConditionSerializer,
    CreateConditionSerializer)
from .cuotas import (
    ListCuotaSerializer,
    CreateCuotaSerializer)
from .empleadores import CreateEmpleadorSerializer
from .empresas_compradoras import (
    EmpresaCompradoraSerializer,
    CreateEmpresaCompradoraSerializer)
from ventas.serializers.ventas_logs import VentaLogSerializer


class ListReservaInmuebleSerializer(serializers.ModelSerializer):
    InmuebleID = serializers.CharField(
        source='InmuebleID.InmuebleID'
    )
    InmuebleType = serializers.CharField(
        source='InmuebleID.InmuebleTypeID.Name'
    )
    Number = serializers.CharField(
        source='InmuebleID.Number'
    )
    Floor = serializers.CharField(
        source='InmuebleID.Floor'
    )
    Tipologia = serializers.CharField(
        source='InmuebleID.TipologiaID.Name',
        allow_null=True
    )
    Price = serializers.DecimalField(
        source='InmuebleID.Price',
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    Discount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    BedroomsQuantity = serializers.IntegerField(
        source='InmuebleID.BedroomsQuantity',
        read_only=True
    )
    BathroomQuantity = serializers.IntegerField(
        source='InmuebleID.BathroomQuantity',
        read_only=True
    )
    Orientation = ListOrientationSerializer(
        source='InmuebleID.OrientationID',
        many=True,
        read_only=True
    )
    Restrictions = serializers.SerializerMethodField('get_restrictions')

    class Meta:
        model = ReservaInmueble
        fields = ('InmuebleID', 'InmuebleType',
                  'Number', 'Floor', 'Tipologia', 'Price', 'BedroomsQuantity',
                  'BathroomQuantity', 'Orientation', 'Discount', 'Restrictions')

    def get_restrictions(self, obj):
        restrictions = InmuebleInmueble.objects.filter(InmuebleAID=obj.InmuebleID).select_related('InmuebleAID',
                                                                                                  'InmuebleBID',
                                                                                                  'InmuebleInmuebleTypeID')
        data = [RestrictionSerializer(restriction).to_dict() for restriction in restrictions]
        return data


class ListReservaSerializer(serializers.ModelSerializer):
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )
    Proyecto = serializers.CharField(
        source='ProyectoID.Name'
    )
    ReservaState = serializers.CharField(
        source='ReservaStateID.Name'
    )
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
    Inmuebles = serializers.SerializerMethodField('get_inmuebles')
    Date = serializers.SerializerMethodField('get_date')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ProyectoID', 'ClienteID', 'ReservaStateID')
        return queryset

    class Meta:
        model = Reserva
        fields = ('ReservaID', 'ProyectoID', 'Proyecto', 'ClienteID', 'Date',
                  'ClienteName', 'ClienteLastNames', 'ClienteRut', 'Folio',
                  'ReservaState', 'Inmuebles')

    def get_inmuebles(self, obj):
        inmuebles_reserva = ReservaInmueble.objects.filter(ReservaID=obj).prefetch_related(
            'InmuebleID__InmuebleRestrict')
        serializer = ListReservaInmuebleSerializer(instance=inmuebles_reserva, many=True)
        return serializer.data

    def get_date(self, obj):
        try:
            return obj.Date.strftime("%Y-%m-%d")
        except AttributeError:
            return ""


class RetrieveReservaSerializer(serializers.ModelSerializer):
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
    Condition = ConditionSerializer(
        source='ConditionID',
        many=True,
        allow_null=True
    )
    CotizacionType = serializers.CharField(
        source='CotizacionTypeID.Name',
        allow_null=True
    )
    ClienteID = serializers.UUIDField(
        source='ClienteID.UserID',
        allow_null=True
    )
    Cliente = ClienteSerializer(
        source='ClienteID',
        allow_null=True
    )
    VendedorID = serializers.UUIDField(
        source='VendedorID.UserID',
        allow_null=True
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
    ReservaState = serializers.CharField(
        source='ReservaStateID.Name',
        allow_null=True
    )
    PayType = serializers.CharField(
        source='PayTypeID.Name',
        allow_null=True
    )
    Cuotas = ListCuotaSerializer(
        source='CuotaID',
        many=True,
        allow_null=True
    )
    ContactMethodType = serializers.CharField(
        source='ContactMethodTypeID.Name',
        allow_null=True
    )
    ContactMethodTypeID = serializers.CharField(
        source='ContactMethodTypeID.ContactMethodTypeID'
    )
    PaymentFirmaPromesa = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True,
        allow_null=True
    )
    PaymentFirmaEscritura = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True,
        allow_null=True
    )
    PaymentInstitucionFinanciera = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True,
        allow_null=True
    )
    AhorroPlus = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True,
        allow_null=True
    )
    Inmuebles = serializers.SerializerMethodField('get_inmuebles')
    Documents = serializers.SerializerMethodField('get_documents')
    IsFinished = serializers.SerializerMethodField('get_state_reserva')
    Graph = serializers.SerializerMethodField('get_graph')
    Patrimony = serializers.SerializerMethodField('get_patrimony')
    Logs = serializers.SerializerMethodField('get_logs')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ProyectoID',
            'ClienteID',
            'VendedorID',
            'ReservaStateID',
            'CodeudorID',
            'PayTypeID',
            'ContactMethodTypeID',
            'EmpresaCompradoraID')
        queryset = queryset.prefetch_related(
            'CuotaID', 'InmuebleID', 'ConditionID')
        return queryset

    class Meta:
        model = Reserva
        fields = (
            'ReservaID',
            'ProyectoID',
            'Proyecto',
            'CotizacionType',
            'ClienteID',
            'Date',
            'Cliente',
            'EmpresaCompradora',
            'VendedorID',
            'Vendedor',
            'CodeudorID',
            'Codeudor',
            'Folio',
            'ReservaState',
            'PayType',
            'ContactMethodType',
            'ContactMethodTypeID',
            'DateFirmaPromesa',
            'PaymentFirmaPromesa',
            'PaymentFirmaEscritura',
            'PaymentInstitucionFinanciera',
            'AhorroPlus',
            'IsNotInvestment',
            'Condition',
            'Cuotas',
            'Inmuebles',
            'Documents',
            'IsFinished',
            'Graph',
            'Patrimony',
            'Logs')

    def get_patrimony(self, obj):
        patrimonies = Patrimony.objects.filter(ClienteID=obj.ClienteID)
        if patrimonies.exists():
            return PatrimonySerializer(instance=patrimonies[0]).data
        return None

    def get_inmuebles(self, obj):
        inmuebles_reserva = ReservaInmueble.objects.filter(
            ReservaID=obj)
        serializer = ListReservaInmuebleSerializer(
            instance=inmuebles_reserva, many=True)
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
        if obj.ReservaStateID.Name == constants.RESERVA_STATE[2]:
            return {}
        else:
            return graph

    def get_state_reserva(self, obj):
        if obj.ReservaStateID.Name == constants.RESERVA_STATE[2]:
            return True
        else:
            return False

    def get_logs(self, obj):
        venta_log = VentaLog.objects.filter(
            # VentaLogTypeID__in=VentaLogType.objects.filter(Name__in=constants.VENTA_LOG_TYPE),
            Folio=obj.Folio).order_by('-id')
        serializer = VentaLogSerializer(instance=venta_log, many=True)
        return serializer.data


class CreateReservaInmuebleSerializer(serializers.ModelSerializer):
    InmuebleID = serializers.UUIDField(
        write_only=True
    )
    Discount = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True
    )

    class Meta:
        model = ReservaInmueble
        fields = ('InmuebleID', 'Discount')


class CreateReservaSerializer(serializers.ModelSerializer):
    EmpresaCompradora = CreateEmpresaCompradoraSerializer(
        source='EmpresaCompradoraID',
        required=False,
        allow_null=True
    )
    CotizacionType = serializers.CharField(
        write_only=True
    )
    Condition = CreateConditionSerializer(
        source='ConditionID',
        many=True,
        required=False
    )
    ProyectoID = serializers.UUIDField(
        write_only=True
    )
    CotizacionID = serializers.UUIDField(
        write_only=True,
        required=False,
        allow_null=True
    )
    Cliente = CreateClienteCotizacionSerializer(
        required=False,
        allow_null=True
    )
    CodeudorID = serializers.CharField(
        write_only=True,
        allow_null=True,
        required=False
    )
    Codeudor = CreateClienteCotizacionSerializer(
        required=False,
        allow_null=True
    )
    PayType = serializers.CharField(
        write_only=True,
        required=False
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
    ContactMethodTypeID = serializers.UUIDField(
        write_only=True,
        required=False
    )
    PaymentFirmaPromesa = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        required=False
    )
    PaymentFirmaEscritura = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        required=False
    )
    PaymentInstitucionFinanciera = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True,
        required=False
    )
    AhorroPlus = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True,
        required=False
    )
    DateFirmaPromesa = serializers.DateTimeField(
        write_only=True,
        allow_null=True,
        required=False
    )
    Empleador = CreateEmpleadorSerializer(
        write_only=True,
        required=False
    )

    CoEmpleador = CreateEmpleadorSerializer(
        write_only=True,
        required=False
    )

    Patrimony = PatrimonySerializer(
        required=False,
        allow_null=True
    )
    ValueProductoFinanciero = serializers.IntegerField(
        write_only=True,
        required=False
    )
    Date8 = serializers.BooleanField(
        required=False,
    )
    Date10 = serializers.BooleanField(
        required=False,
    )
    Date15 = serializers.BooleanField(
        required=False,
    )
    Date20 = serializers.BooleanField(
        required=False,
    )
    Date25 = serializers.BooleanField(
        required=False,
    )
    Date30 = serializers.BooleanField(
        required=False,
    )
    Folio = serializers.CharField(required=False)

    class Meta:
        model = Reserva
        fields = (
            'ProyectoID',
            'Condition',
            'CotizacionType',
            'Cliente',
            'CotizacionID',
            'CodeudorID',
            'Codeudor',
            'PayType',
            'EmpresaCompradora',
            'Cuotas',
            'Inmuebles',
            'Folio',
            'ContactMethodTypeID',
            'IsNotInvestment',
            'PaymentFirmaPromesa',
            'PaymentFirmaEscritura',
            'PaymentInstitucionFinanciera',
            'AhorroPlus',
            'DateFirmaPromesa',
            'Empleador',
            'CoEmpleador',
            'Patrimony',
            'ValueProductoFinanciero',
            'Date8',
            'Date10',
            'Date15',
            'Date20',
            'Date25',
            'Date30')

    def create(self, validated_data):
        current_user = return_current_user(self)
        miss_info = False
        proyecto_id = validated_data['ProyectoID']
        contact_method_type_id = validated_data.get('ContactMethodTypeID')
        codeudor_id = validated_data.get('CodeudorID')
        cotizacion_id = validated_data.get('CotizacionID')
        pay_type_name = validated_data.get('PayType')
        date_firma_promesa = validated_data.get('DateFirmaPromesa')
        value_producto_financiero = validated_data.get('ValueProductoFinanciero')

        empresa_compradora_data = validated_data.get('EmpresaCompradoraID')

        if validated_data['CotizacionType']:
            cotizacion_type = CotizacionType.objects.get(
                Name=validated_data['CotizacionType'])
        else:
            cotizacion_type = None

        if empresa_compradora_data:
            razon_social_empresa_compradora = empresa_compradora_data['RazonSocial']
            rut_empresa_compradora = empresa_compradora_data['Rut']
            direccion_empresa_compradora = empresa_compradora_data['Address']
        else:
            rut_empresa_compradora = direccion_empresa_compradora = razon_social_empresa_compradora = None

        inmuebles_data = validated_data.get('InmuebleID', [])
        cuotas_data = validated_data.get('CuotaID')
        conditions_data = validated_data.get('ConditionID')
        patrimony_data = validated_data.get('Patrimony')
        cliente_data = validated_data.get('Cliente')
        codeudor_data = validated_data.get('Codeudor')

        empleador_data = validated_data.get('Empleador')
        if empleador_data:
            rut_empleador = empleador_data['Rut']
            razon_social_empleador = empleador_data['RazonSocial']
        else:
            razon_social_empleador = rut_empleador = None

        co_empleador_data = validated_data.get('CoEmpleador')
        if co_empleador_data:
            rut_co_empleador = co_empleador_data['Rut']
            razon_social_co_empleador = co_empleador_data['RazonSocial']
        else:
            rut_co_empleador = razon_social_co_empleador = None

        pay_type = get_or_none(PayType, Name=pay_type_name)

        # Plazos a imprimir en simulador de credito
        date_8 = validated_data.get('Date8')
        date_10 = validated_data.get('Date10')
        date_15 = validated_data.get('Date15')
        date_20 = validated_data.get('Date20')
        date_25 = validated_data.get('Date25')
        date_30 = validated_data.get('Date30')

        # Validaciones campos comunes entre ambos tipos de cliente
        if pay_type_name and not pay_type:
            raise CustomValidation(
                "Debe ingresar tipo de pago",
                status_code=status.HTTP_409_CONFLICT)

        if empresa_compradora_data:
            if not razon_social_empresa_compradora:
                razon_social_empresa_compradora = ""
                miss_info = True

            if not rut_empresa_compradora:
                rut_empresa_compradora = ""
                miss_info = True

            if not direccion_empresa_compradora:
                direccion_empresa_compradora = ""
                miss_info = True

        if cliente_data:
            cliente = Cliente.objects.get(Rut=cliente_data['Rut'])
        else:
            cliente = Cliente()

        cliente = save_cliente_return(cliente_data, cliente, current_user)

        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)

        if contact_method_type_id:
            contact_method_type = ContactMethodType.objects.get(
                ContactMethodTypeID=contact_method_type_id)
        else:
            contact_method_type = None

        if cotizacion_id:
            cotizacion = Cotizacion.objects.get(CotizacionID=cotizacion_id)
            cotizacion_state = CotizacionState.objects.get(
                Name=constants.COTIZATION_STATE[2])
            cotizacion.CotizacionStateID = cotizacion_state
            cotizacion.save()

        if empresa_compradora_data:
            empresa_compradora = EmpresaCompradora.objects.filter(ClienteID=cliente)
            if len(empresa_compradora) > 0:
                empresa_compradora = empresa_compradora[0]
            else:
                empresa_compradora = EmpresaCompradora()
            empresa_compradora.RazonSocial = razon_social_empresa_compradora
            empresa_compradora.Address = direccion_empresa_compradora
            empresa_compradora.Rut = rut_empresa_compradora
            empresa_compradora.ClienteID = cliente
            empresa_compradora.save()
        else:
            empresa_compradora = None

        patrimony = get_or_none(Patrimony, ClienteID=cliente)

        if patrimony_data:
            default_ = {
                "Pasivos": 0,
                "PagosMensuales": 0,
                "Saldo": 0
            }
            if patrimony:
                patrimony.RealState = patrimony_data.get('RealState', 0)
                patrimony.Vehicle = patrimony_data.get('Vehicle', 0)
                patrimony.DownPayment = patrimony_data.get('DownPayment', 0)
                patrimony.Other = patrimony_data.get('Other', 0)
                patrimony.CreditCard = patrimony_data.get('CreditCard', default_)
                patrimony.CreditoConsumo = patrimony_data.get('CreditoConsumo', default_)
                patrimony.CreditoHipotecario = patrimony_data.get('CreditoHipotecario', default_)
                patrimony.PrestamoEmpleador = patrimony_data.get('PrestamoEmpleador', default_)
                patrimony.CreditoComercio = patrimony_data.get('CreditoComercio', default_)
                patrimony.DeudaIndirecta = patrimony_data.get('DeudaIndirecta', default_)
                patrimony.AnotherCredit = patrimony_data.get('AnotherCredit', default_)
                patrimony.Deposits = patrimony_data.get('Deposits', 0)
                patrimony.Rent = patrimony_data.get('Rent', 0)

                patrimony.save()
            else:
                patrimony = Patrimony.objects.create(
                    ClienteID=cliente,
                    RealState=patrimony_data.get('RealState', 0),
                    Vehicle=patrimony_data.get('Vehicle', 0),
                    DownPayment=patrimony_data.get('DownPayment', 0),
                    Other=patrimony_data.get('Other', 0),
                    CreditCard=patrimony_data.get('CreditCard', default_),
                    CreditoConsumo=patrimony_data.get('CreditoConsumo', default_),
                    CreditoHipotecario=patrimony_data.get('CreditoHipotecario', default_),
                    PrestamoEmpleador=patrimony_data.get('PrestamoEmpleador', default_),
                    CreditoComercio=patrimony_data.get('CreditoComercio', default_),
                    DeudaIndirecta=patrimony_data.get('DeudaIndirecta', default_),
                    AnotherCredit=patrimony_data.get('AnotherCredit', default_),
                    Deposits=patrimony_data.get('Deposits', 0)
                )
        else:
            patrimony = None

        if empleador_data:
            empleador = Empleador.objects.filter(ClienteID=cliente)
            if len(empleador) > 0:
                empleador = empleador[0]
            else:
                empleador = Empleador()
            empleador.RazonSocial = razon_social_empleador
            empleador.Rut = rut_empleador
            empleador.ClienteID = cliente
            empleador.Extra = empleador_data['Extra']
            empleador.save()
        else:
            empleador = None

        if codeudor_id:
            codeudor = get_or_none(Cliente, UserID=codeudor_id)
        else:
            codeudor = None

        if codeudor_data and codeudor:
            codeudor = save_cliente_return(codeudor_data, codeudor, current_user)

        if codeudor and co_empleador_data:
            co_empleador = Empleador.objects.filter(ClienteID=cliente)
            if len(co_empleador) > 0:
                co_empleador = co_empleador[0]
            else:
                co_empleador = Empleador()
            co_empleador.RazonSocial = razon_social_co_empleador
            co_empleador.Rut = rut_co_empleador
            co_empleador.ClienteID = codeudor
            co_empleador.Extra = co_empleador_data['Extra']
            co_empleador.save()
        else:
            co_empleador = None

        reserva_state = ReservaState.objects.get(
            Name=constants.RESERVA_STATE[0])

        # if miss_info:
        #    reserva_state = ReservaState.objects.get(
        #        Name=constants.RESERVA_STATE[0])
        # else:
        #    reserva_state = ReservaState.objects.get(
        #        Name=constants.RESERVA_STATE[1])

        folio = validated_data.get('Folio')
        if not folio:
            with transaction.atomic():
                counter_folio = CounterFolio.objects.get(ProyectoID=proyecto)
                counter_folio.Count += 1
                counter_folio.save()
                counter_folio.Count -= 1
            folio = proyecto.Symbol + str(counter_folio.Count)

        reserva_data = dict(ProyectoID=proyecto,
                            ClienteID=cliente,
                            VendedorID=current_user,
                            Folio=folio,
                            CotizacionTypeID=cotizacion_type,
                            CodeudorID=codeudor,
                            EmpresaCompradoraID=empresa_compradora,
                            ReservaStateID=reserva_state,
                            ContactMethodTypeID=contact_method_type,
                            IsNotInvestment=validated_data.get('IsNotInvestment', False),
                            PaymentFirmaPromesa=validated_data.get('PaymentFirmaPromesa'),
                            PaymentFirmaEscritura=validated_data.get('PaymentFirmaEscritura'),
                            PaymentInstitucionFinanciera=validated_data.get('PaymentInstitucionFinanciera'),
                            AhorroPlus=validated_data.get('AhorroPlus'),
                            PayTypeID=pay_type,
                            DateFirmaPromesa=date_firma_promesa,
                            ValueProductoFinanciero=value_producto_financiero)
        instance = Reserva.objects.create(**reserva_data)

        if cuotas_data:
            for cuota_data in cuotas_data:
                cuota = Cuota.objects.create(
                    Amount=cuota_data['Amount'],
                    Date=cuota_data['Date'],
                    Observacion=cuota_data.get('Observacion')
                )
                instance.CuotaID.add(cuota)

        conditions = list()

        if conditions_data:
            for condition_data in conditions_data:
                condition = Condition.objects.create(
                    Description=condition_data['Description']
                )
                instance.ConditionID.add(condition)
                conditions.append(condition)

        reserva_inmuebles = list()
        total = 0
        total_uf = 0
        total_cuotas = 0

        for inmueble_data in inmuebles_data:
            inmueble = Inmueble.objects.get(
                InmuebleID=inmueble_data['InmuebleID']
            )
            inmueble_state = InmuebleState.objects.get(
                Name=constants.INMUEBLE_STATE[2]
            )
            if inmueble_data['Discount']:
                discount = inmueble_data['Discount']
                price_discount = round(
                    inmueble.Price *
                    discount /
                    100,
                    2)
                price = inmueble.Price - price_discount
                total_uf += price
            else:
                discount = 0
                total_uf += inmueble.Price

            inmueble.InmuebleStateID = inmueble_state
            inmueble.save()

            reserva_inmueble = ReservaInmueble()
            reserva_inmueble.ReservaID = instance
            reserva_inmueble.InmuebleID = inmueble
            reserva_inmueble.Discount = discount

            reserva_inmuebles.append(reserva_inmueble)

        ReservaInmueble.objects.bulk_create(reserva_inmuebles)

        if instance.CuotaID.all():
            for cuota in instance.CuotaID.all():
                total_cuotas += cuota.Amount

            total_cuotas_solas = total_cuotas
            porcentaje_cuotas = (total_cuotas * 100) / total_uf
            total += total_cuotas
        else:
            total_cuotas_solas = 0
            porcentaje_cuotas = 0

        if instance.PaymentFirmaEscritura:
            total += instance.PaymentFirmaEscritura
            porcentaje_firma = (instance.PaymentFirmaEscritura * 100) / total_uf
        else:
            porcentaje_firma = 0

        if instance.PaymentInstitucionFinanciera:
            total += instance.PaymentInstitucionFinanciera
            porcentaje_credito = (instance.PaymentInstitucionFinanciera * 100) / total_uf
        else:
            porcentaje_credito = 0

        if instance.PaymentFirmaEscritura and instance.PaymentFirmaPromesa:
            total_contado = total_cuotas_solas + instance.PaymentFirmaEscritura + instance.PaymentFirmaPromesa
            porcentaje_contado = (total_contado * 100) / total_uf
        else:
            total_contado = 0
            porcentaje_contado = 0

        if instance.AhorroPlus:
            total += instance.AhorroPlus
            porcentaje_ahorro_plus = (instance.AhorroPlus * 100) / total_uf
        else:
            porcentaje_ahorro_plus = 0

        phone = get_object_or_404(ContactInfoType, Name='Phone')
        email = get_object_or_404(ContactInfoType, Name='Email')

        phones = ClienteContactInfo.objects.filter(UserID=cliente, ContactInfoTypeID=phone)
        emails = ClienteContactInfo.objects.filter(UserID=cliente, ContactInfoTypeID=email)

        if phones.exists():
            phone_value = phones[0].Value
        else:
            phone_value = str()
        if emails.exists():
            email_value = emails[0].Value
        else:
            email_value = str()
        # Crear pdf oferta
        context_dict = {
            'reserva': instance,
            'corredores': constants.COMPANY_NAME[1],
            'cliente': cliente,
            'telefono': phone_value,
            'proyecto': proyecto,
            'inmuebles_a_reservar': reserva_inmuebles,
            'total_uf': total_uf,
            'total_cuotas': total_cuotas_solas,
            'total_firma': instance.PaymentFirmaEscritura,
            'porcentaje_cuotas': porcentaje_cuotas,
            'porcentaje_firma': porcentaje_firma,
            'porcentaje_credito': porcentaje_credito,
            'porcentaje_ahorro_plus': porcentaje_ahorro_plus,
            'ahorro_plus': instance.AhorroPlus,
            'total_credito': instance.PaymentInstitucionFinanciera,
            'total_pago': total,
            'conditions': conditions,
            'tamaño_letra': 100,
            'gestion': constants.COMPANY_NAME[0]
        }

        oferta_pdf = render_create_oferta_to_pdf(context_dict)
        filename = "%s_OFE_%s.pdf" % (instance.Folio, cliente)
        oferta_pdf_generated = ContentFile(oferta_pdf)
        oferta_pdf_generated.name = filename

        if pay_type and pay_type.Name == constants.PAY_TYPE[1]:
            # Crear pdf ficha
            totals = calculate_totals_patrimony(patrimony)
            context_dict = {
                'reserva': instance,
                'cliente': cliente,
                'correo': email_value,
                'telefono': phone_value,
                'inmuebles_a_reservar': reserva_inmuebles,
                'proyecto': proyecto,
                'empleador': empleador,
                'total_uf': total_uf,
                'porcentaje_credito': porcentaje_credito,
                'porcentaje_contado': porcentaje_contado,
                'total_credito': instance.PaymentInstitucionFinanciera,
                'total_contado': total_contado,
                'porcentaje_ahorro_plus': porcentaje_ahorro_plus,
                'ahorro_plus': instance.AhorroPlus,
                'gestion': constants.COMPANY_NAME[0],
                'patrimonio': patrimony,
                'totals': totals,
                'tamaño_letra': 100
            }

            ficha_pdf = render_create_ficha_to_pdf(context_dict)
            filename = "%s_FPA_%s.pdf" % (instance.Folio, cliente)
            ficha_pdf_generated = ContentFile(ficha_pdf)
            ficha_pdf_generated.name = filename

            # Crear pdf simulador

            rate = ConstantNumeric.objects.get(Name__iexact=constants.SEARCH_NAME_CONSTANT_NUMERIC[0])
            has_codeudor = True if codeudor else False

            if date_8:
                values_8 = calculate_simulate_values(total_uf, porcentaje_credito, rate.Value, 8, has_codeudor)
            else:
                values_8 = None
            if date_10:
                values_10 = calculate_simulate_values(total_uf, porcentaje_credito, rate.Value, 10, has_codeudor)
            else:
                values_10 = None
            if date_15:
                values_15 = calculate_simulate_values(total_uf, porcentaje_credito, rate.Value, 15, has_codeudor)
            else:
                values_15 = None
            if date_20:
                values_20 = calculate_simulate_values(total_uf, porcentaje_credito, rate.Value, 20, has_codeudor)
            else:
                values_20 = None
            if date_25:
                values_25 = calculate_simulate_values(total_uf, porcentaje_credito, rate.Value, 25, has_codeudor)
            else:
                values_25 = None
            if date_30:
                values_30 = calculate_simulate_values(total_uf, porcentaje_credito, rate.Value, 30, has_codeudor)
            else:
                values_30 = None

            context_dict = {
                'reserva': instance,
                'cliente': cliente,
                'inmuebles_a_reservar': reserva_inmuebles,
                'proyecto': proyecto,
                'uf': valor_uf_actual(),
                'gestion': constants.COMPANY_NAME[0],
                'total_uf': total_uf,
                'total_credito': instance.PaymentInstitucionFinanciera,
                'porcentaje_credito': porcentaje_credito,
                'porcentaje_ahorro_plus': porcentaje_ahorro_plus,
                'ahorro_plus': instance.AhorroPlus,
                'rate': rate.Value,
                'values_8': values_8,
                'values_10': values_10,
                'values_15': values_15,
                'values_20': values_20,
                'values_25': values_25,
                'values_30': values_30,
                'tamaño_letra': 100,
            }

            simulador_pdf = render_create_simulador_to_pdf(context_dict)
            filename = "%s_SDC_%s.pdf" % (instance.Folio, cliente)
            simulador_pdf_generated = ContentFile(simulador_pdf)
            simulador_pdf_generated.name = filename
        else:
            ficha_pdf_generated = None
            simulador_pdf_generated = None

        # Crear notificaciones
        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])
        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=proyecto, UserProyectoTypeID=jefe_proyecto_type)

        if miss_info:
            crear_notificacion_reserva_pendiente_informacion(
                instance, jefe_proyecto, current_user)
        else:
            asistente_comercial_type = UserProyectoType.objects.get(
                Name=constants.USER_PROYECTO_TYPE[3])
            asistente_comercial = UserProyecto.objects.filter(
                ProyectoID=proyecto, UserProyectoTypeID=asistente_comercial_type)

            crear_notificacion_reserva_pendiente_control(
                instance, jefe_proyecto, asistente_comercial)

        # Registro Bitacora de Ventas
        venta_log_type = VentaLogType.objects.get(
            Name=constants.VENTA_LOG_TYPE[0])

        VentaLog.objects.create(
            VentaID=instance.ReservaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=cliente,
            ProyectoID=proyecto,
            VentaLogTypeID=venta_log_type,
        )

        try:
            documents = get_object_or_404(DocumentVenta, Folio=instance.Folio)
            documents.DocumentOferta = oferta_pdf_generated
            documents.DocumentFichaPreAprobacion = ficha_pdf_generated
            documents.DocumentSimulador = simulador_pdf_generated
            documents.save()
        except:
            DocumentVenta.objects.create(
                Folio=instance.Folio,
                DocumentOferta=oferta_pdf_generated,
                DocumentFichaPreAprobacion=ficha_pdf_generated,
                DocumentSimulador=simulador_pdf_generated,
            )
        return instance


class UpdateReservaSerializer(serializers.ModelSerializer):
    EmpresaCompradora = CreateEmpresaCompradoraSerializer(
        source='EmpresaCompradoraID',
        allow_null=True,
        required=False
    )
    Condition = CreateConditionSerializer(
        source='ConditionID',
        many=True,
        required=False
    )
    ProyectoID = serializers.UUIDField(
        write_only=True,
        required=False
    )
    CotizacionID = serializers.UUIDField(
        write_only=True,
        required=False
    )
    ClienteID = serializers.UUIDField(
        write_only=True,
        required=False
    )
    Cliente = CreateClienteCotizacionSerializer(
        required=False,
        allow_null=True
    )
    CodeudorID = serializers.UUIDField(
        write_only=True,
        allow_null=True,
        required=False
    )
    Codeudor = CreateClienteCotizacionSerializer(
        required=False,
        allow_null=True
    )
    PayType = serializers.CharField(
        write_only=True,
        required=False
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
    ContactMethodTypeID = serializers.UUIDField(
        write_only=True,
        required=False
    )
    Patrimony = PatrimonySerializer(
        required=False,
        allow_null=True,
    )
    PaymentFirmaPromesa = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        required=False
    )
    PaymentFirmaEscritura = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        required=False
    )
    PaymentInstitucionFinanciera = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True,
        required=False
    )
    AhorroPlus = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True,
        required=False
    )
    DateFirmaPromesa = serializers.DateTimeField(
        write_only=True,
        allow_null=True,
        required=False
    )
    Empleador = CreateEmpleadorSerializer(
        write_only=True,
        required=False
    )
    CoEmpleador = CreateEmpleadorSerializer(
        write_only=True,
        required=False
    )
    ValueProductoFinanciero = serializers.IntegerField(
        write_only=True,
        required=False
    )
    Extra = serializers.JSONField(
        write_only=True,
        required=False
    )
    Date8 = serializers.BooleanField(
        required=False,
    )
    Date10 = serializers.BooleanField(
        required=False,
    )
    Date15 = serializers.BooleanField(
        required=False,
    )
    Date20 = serializers.BooleanField(
        required=False,
    )
    Date25 = serializers.BooleanField(
        required=False,
    )
    Date30 = serializers.BooleanField(
        required=False,
    )

    class Meta:
        model = Reserva
        fields = (
            'ProyectoID',
            'Condition',
            'ClienteID',
            'Cliente',
            'CotizacionID',
            'CodeudorID',
            'Codeudor',
            'PayType',
            'Cuotas',
            'Inmuebles',
            'EmpresaCompradora',
            'ContactMethodTypeID',
            'Patrimony',
            'PaymentFirmaPromesa',
            'PaymentFirmaEscritura',
            'PaymentInstitucionFinanciera',
            'AhorroPlus',
            'DateFirmaPromesa',
            'Empleador',
            'CoEmpleador',
            'ValueProductoFinanciero',
            'Extra',
            'Date8',
            'Date10',
            'Date15',
            'Date20',
            'Date25',
            'Date30')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        miss_info = False
        if instance.ReservaStateID.Name == constants.RESERVA_STATE[2]:
            raise CustomValidation(
                "Reserva en estado oferta, debe modificar oferta",
                status_code=status.HTTP_409_CONFLICT)

        proyecto_id = validated_data['ProyectoID']
        cliente_id = validated_data.get('ClienteID', False)
        contact_method_type_id = validated_data.get('ContactMethodTypeID', False)
        codeudor_id = validated_data.get('CodeudorID', False)
        cotizacion_id = validated_data.get('CotizacionID', False)
        pay_type_name = validated_data.get('PayType', False)
        date_firma_promesa = validated_data.get('DateFirmaPromesa', False)
        value_producto_financiero = validated_data.get('ValueProductoFinanciero', False)

        empresa_compradora_data = validated_data.get('EmpresaCompradoraID', False)
        if empresa_compradora_data:
            razon_social_empresa_compradora = empresa_compradora_data['RazonSocial']
            rut_empresa_compradora = empresa_compradora_data['Rut']
            direccion_empresa_compradora = empresa_compradora_data['Address']
        else:
            razon_social_empresa_compradora = rut_empresa_compradora = direccion_empresa_compradora = False

        inmuebles_data = validated_data.get('InmuebleID', [])
        cuotas_data = validated_data.get('CuotaID', False)
        conditions_data = validated_data.get('ConditionID', False)
        patrimony_data = validated_data.get('Patrimony', False)
        empleador_data = validated_data.get('Empleador', False)
        if empleador_data:
            rut_empleador = empleador_data['Rut']
            razon_social_empleador = empleador_data['RazonSocial']
            extra_empleador = empleador_data['Extra']
        else:
            rut_empleador = razon_social_empleador = False

        co_empleador_data = validated_data.get('CoEmpleador', False)
        if co_empleador_data:
            rut_co_empleador = co_empleador_data['Rut']
            razon_social_co_empleador = co_empleador_data['RazonSocial']
            extra_co_empleador = co_empleador_data['Extra']
        else:
            rut_co_empleador = razon_social_co_empleador = False

            # Plazos a imprimir en simulador de credito
        date_8 = validated_data.get('Date8', False)
        date_10 = validated_data.get('Date10', False)
        date_15 = validated_data.get('Date15', False)
        date_20 = validated_data.get('Date20', False)
        date_25 = validated_data.get('Date25', False)
        date_30 = validated_data.get('Date30', False)

        if pay_type_name is not False:
            pay_type = get_or_none(PayType, Name=pay_type_name)
        else:
            pay_type = False

        if pay_type_name == "Credito":
            if not rut_empleador:
                rut_empleador = ""
                miss_info = True

            if not razon_social_empleador:
                razon_social_empleador = ""
                miss_info = True

        if empresa_compradora_data:
            if not razon_social_empresa_compradora:
                razon_social_empresa_compradora = ""
                miss_info = True

            if not rut_empresa_compradora:
                rut_empresa_compradora = ""
                miss_info = True

            if not direccion_empresa_compradora:
                direccion_empresa_compradora = ""
                miss_info = True

        if cliente_id:
            cliente = Cliente.objects.get(UserID=cliente_id)
        else:
            cliente = None
        if proyecto_id:
            proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        else:
            proyecto = None
        if contact_method_type_id:
            contact_method_type = ContactMethodType.objects.get(
                ContactMethodTypeID=contact_method_type_id)
        else:
            contact_method_type = None
        if cotizacion_id:
            cotizacion = Cotizacion.objects.get(CotizacionID=cotizacion_id)
        else:
            cotizacion = None

        if 'Cliente' in validated_data:
            cliente = save_cliente_return(validated_data['Cliente'], cliente, current_user)
            instance.ClienteID = cliente

        if codeudor_id:
            codeudor = Cliente.objects.get(UserID=codeudor_id)
        else:
            codeudor = None

        if 'Codeudor' in validated_data and codeudor:
            codeudor = save_cliente_return(validated_data['Codeudor'], codeudor, current_user)
            instance.CodeudorID = codeudor

        if empresa_compradora_data:
            empresa_compradora = EmpresaCompradora.objects.filter(ClienteID=cliente)
            if len(empresa_compradora) > 0:
                empresa_compradora = empresa_compradora[0]
            else:
                empresa_compradora = EmpresaCompradora()
            empresa_compradora.RazonSocial = razon_social_empresa_compradora
            empresa_compradora.Address = direccion_empresa_compradora
            empresa_compradora.Rut = rut_empresa_compradora
            empresa_compradora.ClienteID = cliente
            empresa_compradora.save()
        else:
            empresa_compradora = None

        if cliente is not False:
            patrimony = get_or_none(Patrimony, ClienteID=cliente)
        else:
            patrimony = None

        if patrimony_data is not False:
            default_ = {
                "Pasivos": 0,
                "PagosMensuales": 0,
                "Saldo": 0
            }
            if patrimony:
                patrimony.RealState = patrimony_data.get('RealState', 0)
                patrimony.Vehicle = patrimony_data.get('Vehicle', 0)
                patrimony.DownPayment = patrimony_data.get('DownPayment', 0)
                patrimony.Other = patrimony_data.get('Other', 0)
                patrimony.CreditCard = patrimony_data.get('CreditCard', default_)
                patrimony.CreditoConsumo = patrimony_data.get('CreditoConsumo', default_)
                patrimony.CreditoHipotecario = patrimony_data.get('CreditoHipotecario', default_)
                patrimony.PrestamoEmpleador = patrimony_data.get('PrestamoEmpleador', default_)
                patrimony.CreditoComercio = patrimony_data.get('CreditoComercio', default_)
                patrimony.DeudaIndirecta = patrimony_data.get('DeudaIndirecta', default_)
                patrimony.AnotherCredit = patrimony_data.get('AnotherCredit', default_)
                patrimony.Deposits = patrimony_data.get('Deposits', 0)
                patrimony.Rent = patrimony_data.get('Rent', 0)
                patrimony.save()
            else:
                patrimony = Patrimony.objects.create(
                    ClienteID=cliente,
                    RealState=patrimony_data.get('RealState', 0),
                    Vehicle=patrimony_data.get('Vehicle', 0),
                    DownPayment=patrimony_data.get('DownPayment', 0),
                    Other=patrimony_data.get('Other', 0),
                    CreditCard=patrimony_data.get('CreditCard', default_),
                    CreditoConsumo=patrimony_data.get('CreditoConsumo', default_),
                    CreditoHipotecario=patrimony_data.get('CreditoHipotecario', default_),
                    PrestamoEmpleador=patrimony_data.get('PrestamoEmpleador', default_),
                    CreditoComercio=patrimony_data.get('CreditoComercio', default_),
                    DeudaIndirecta=patrimony_data.get('DeudaIndirecta', default_),
                    AnotherCredit=patrimony_data.get('AnotherCredit', default_),
                    Deposits=patrimony_data.get('Deposits', 0),
                    Rent=patrimony_data.get('Rent', 0)
                )
        else:
            patrimony = None

        empleador = 0
        # if pay_type_name == "Credito":
        if empleador_data:
            empleador = Empleador.objects.filter(ClienteID=cliente)
            if len(empleador) > 0:
                empleador = empleador[0]
            else:
                empleador = Empleador()
            empleador.ClienteID = cliente
            empleador.Rut = rut_empleador
            empleador.RazonSocial = razon_social_empleador
            empleador.Extra = extra_empleador
            empleador.save()

        if codeudor and co_empleador_data:
            co_empleador = Empleador.objects.filter(ClienteID=codeudor)
            if len(co_empleador) > 0:
                co_empleador = co_empleador[0]
            else:
                co_empleador = Empleador()
            co_empleador.ClienteID = codeudor
            co_empleador.Rut = rut_co_empleador
            co_empleador.RazonSocial = razon_social_co_empleador
            co_empleador.Extra = extra_co_empleador
            co_empleador.save()

        reserva_state = ReservaState.objects.get(
            Name=constants.RESERVA_STATE[0])

        # if miss_info:
        #    reserva_state = ReservaState.objects.get(
        #        Name=constants.RESERVA_STATE[0])
        # else:
        #    reserva_state = ReservaState.objects.get(
        #        Name=constants.RESERVA_STATE[1])

        instance.VendedorID = current_user
        if codeudor_id is not False:
            instance.CodeudorID = codeudor
        if empresa_compradora_data is not False:
            instance.EmpresaCompradoraID = empresa_compradora

        instance.ReservaStateID = reserva_state
        if contact_method_type_id is not False:
            instance.ContactMethodTypeID = contact_method_type
        if 'PaymentFirmaPromesa' in validated_data:
            instance.PaymentFirmaPromesa = validated_data['PaymentFirmaPromesa']
        if 'PaymentFirmaEscritura' in validated_data:
            instance.PaymentFirmaEscritura = validated_data['PaymentFirmaEscritura']
        if 'PaymentInstitucionFinanciera' in validated_data:
            instance.PaymentInstitucionFinanciera = validated_data['PaymentInstitucionFinanciera']
        if 'AhorroPlus' in validated_data:
            instance.AhorroPlus = validated_data['AhorroPlus']
        if pay_type_name is not False:
            instance.PayTypeID = pay_type
        if date_firma_promesa is not False:
            instance.DateFirmaPromesa = date_firma_promesa
        if value_producto_financiero is not False:
            instance.ValueProductoFinanciero = value_producto_financiero

        if cuotas_data is not False and cuotas_data is not None:
            cuotas = Cuota.objects.filter(
                cuota_reserva=instance
            )
            if cuotas.exists():
                cuotas.delete()

            instance.CuotaID.clear()

            for cuota_data in cuotas_data:
                cuota = Cuota.objects.create(
                    Amount=cuota_data['Amount'],
                    Date=cuota_data['Date'],
                    Observacion=cuota_data.get('Observacion')
                )
                instance.CuotaID.add(cuota)
        elif cuotas_data is None:
            cuotas = Cuota.objects.filter(
                cuota_reserva=instance
            )
            if cuotas.exists():
                cuotas.delete()

            instance.CuotaID.clear()

        if conditions_data is not False and conditions_data is not None:
            conditions = Condition.objects.filter(
                condition_reserva=instance
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
                condition_reserva=instance
            )
            if conditions.exists():
                conditions.delete()

            instance.ConditionID.clear()
        else:
            conditions = None

        reserva_inmuebles = list()
        total = 0
        total_uf = 0
        total_cuotas = 0

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
                price_discount = round(
                    inmueble.Price *
                    discount /
                    100,
                    2)
                price = inmueble.Price - price_discount
                total_uf += price
            else:
                discount = 0
                total_uf += inmueble.Price

            reserva_inmuebles_qs = ReservaInmueble.objects.filter(
                ReservaID=instance)

            if reserva_inmuebles_qs.exists():
                reserva_inmuebles_qs.delete()

            reserva_inmueble = ReservaInmueble()
            reserva_inmueble.ReservaID = instance
            reserva_inmueble.InmuebleID = inmueble
            reserva_inmueble.Discount = discount

            reserva_inmuebles.append(reserva_inmueble)

        ReservaInmueble.objects.bulk_create(reserva_inmuebles)

        if cotizacion_id:
            cotizacion_state = CotizacionState.objects.get(
                Name=constants.COTIZATION_STATE[2])
            cotizacion.CotizacionStateID = cotizacion_state
            cotizacion.save()

        if instance.CuotaID.all():
            for cuota in instance.CuotaID.all():
                total_cuotas += cuota.Amount

            total_cuotas_solas = total_cuotas
            porcentaje_cuotas = (total_cuotas * 100) / total_uf
            total += total_cuotas
        else:
            total_cuotas_solas = 0
            porcentaje_cuotas = 0

        if instance.AhorroPlus:
            total += instance.AhorroPlus
            try:
                porcentaje_ahorro_plus = (instance.AhorroPlus * 100) / total_uf
            except decimal.DivisionByZero:
                porcentaje_ahorro_plus = 0
        else:
            porcentaje_ahorro_plus = 0

        if instance.PaymentFirmaEscritura:
            total += instance.PaymentFirmaEscritura
            try:
                porcentaje_firma = (instance.PaymentFirmaEscritura * 100) / total_uf
            except decimal.DivisionByZero:
                porcentaje_firma = 0
        else:
            porcentaje_firma = 0
            porcentaje_cuotas = 0

        if instance.PaymentInstitucionFinanciera:
            total += instance.PaymentInstitucionFinanciera
            try:
                porcentaje_credito = (instance.PaymentInstitucionFinanciera * 100) / total_uf
            except decimal.DivisionByZero:
                porcentaje_credito = 0
        else:
            porcentaje_credito = 0

        if instance.PaymentFirmaEscritura and instance.PaymentFirmaPromesa:
            total_contado = total_cuotas_solas + instance.PaymentFirmaEscritura + instance.PaymentFirmaPromesa
            try:
                porcentaje_contado = (total_contado * 100) / total_uf
            except decimal.DivisionByZero:
                porcentaje_contado = 0
        else:
            total_contado = 0
            porcentaje_contado = 0

        phone = get_object_or_404(ContactInfoType, Name='Phone')
        email = get_object_or_404(ContactInfoType, Name='Email')

        phones = ClienteContactInfo.objects.filter(UserID=cliente, ContactInfoTypeID=phone)
        if phones.exists():
            phone_value = phones[0].Value
        else:
            phone_value = str()

        emails = ClienteContactInfo.objects.filter(UserID=cliente, ContactInfoTypeID=email)
        if emails.exists():
            email_value = emails[0].Value
        else:
            email_value = str()
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

        eliminar_notificacion_reserva_informacion_pendiente(instance)

        if miss_info:
            crear_notificacion_reserva_modificada_pendiente_informacion(
                instance, jefe_proyecto, vendedor, asistente_comercial)
        else:
            eliminar_notificacion_reserva_modificada_pendiente_informacion(instance)

            crear_notificacion_reserva_modificada_pendiente_control(
                instance, jefe_proyecto, vendedor, asistente_comercial)

        # Registro Bitacora de Ventas
        venta_log_type = VentaLogType.objects.get(
            Name=constants.VENTA_LOG_TYPE[5])

        VentaLog.objects.create(
            VentaID=instance.ReservaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=cliente,
            ProyectoID=proyecto,
            VentaLogTypeID=venta_log_type,
        )

        # Crear pdf oferta
        context_dict = {
            'reserva': instance,
            'corredores': constants.COMPANY_NAME[1],
            'cliente': cliente,
            'telefono': phone_value,
            'proyecto': proyecto,
            'inmuebles_a_reservar': reserva_inmuebles,
            'total_uf': total_uf,
            'total_cuotas': total_cuotas_solas,
            'total_firma': instance.PaymentFirmaEscritura,
            'porcentaje_cuotas': porcentaje_cuotas,
            'porcentaje_firma': porcentaje_firma,
            'porcentaje_credito': porcentaje_credito,
            'total_credito': instance.PaymentInstitucionFinanciera,
            'total_pago': total,
            'porcentaje_ahorro_plus': porcentaje_ahorro_plus,
            'ahorro_plus': instance.AhorroPlus,
            'conditions': conditions,
            'tamaño_letra': 100,
            'gestion': constants.COMPANY_NAME[0]
        }

        oferta_pdf = render_create_oferta_to_pdf(context_dict)
        filename = "%s_OFE_%s.pdf" % (instance.Folio, cliente)
        oferta_pdf_generated = ContentFile(oferta_pdf)
        oferta_pdf_generated.name = filename

        if pay_type_name and pay_type.Name == constants.PAY_TYPE[1]:
            # Crear pdf ficha
            totals = calculate_totals_patrimony(patrimony)
            context_dict = {
                'reserva': instance,
                'cliente': cliente,
                'correo': email_value,
                'telefono': phone_value,
                'inmuebles_a_reservar': reserva_inmuebles,
                'proyecto': proyecto,
                'empleador': empleador,
                'total_uf': total_uf,
                'porcentaje_credito': porcentaje_credito,
                'porcentaje_contado': porcentaje_contado,
                'total_credito': instance.PaymentInstitucionFinanciera,
                'total_contado': total_contado,
                'porcentaje_ahorro_plus': porcentaje_ahorro_plus,
                'ahorro_plus': instance.AhorroPlus,
                'gestion': constants.COMPANY_NAME[0],
                'patrimonio': patrimony,
                'totals': totals,
                'tamaño_letra': 100
            }

            ficha_pdf = render_create_ficha_to_pdf(context_dict)
            filename = "%s_FPA_%s.pdf" % (instance.Folio, cliente)
            ficha_pdf_generated = ContentFile(ficha_pdf)
            ficha_pdf_generated.name = filename

            # Crear pdf simulador
            rate = ConstantNumeric.objects.get(Name__iexact=constants.SEARCH_NAME_CONSTANT_NUMERIC[0])
            has_codeudor = True if codeudor else False

            if date_8:
                values_8 = calculate_simulate_values(total_uf, porcentaje_credito, rate.Value, 8, has_codeudor)
            else:
                values_8 = None
            if date_10:
                values_10 = calculate_simulate_values(total_uf, porcentaje_credito, rate.Value, 10, has_codeudor)
            else:
                values_10 = None
            if date_15:
                values_15 = calculate_simulate_values(total_uf, porcentaje_credito, rate.Value, 15, has_codeudor)
            else:
                values_15 = None
            if date_20:
                values_20 = calculate_simulate_values(total_uf, porcentaje_credito, rate.Value, 20, has_codeudor)
            else:
                values_20 = None
            if date_25:
                values_25 = calculate_simulate_values(total_uf, porcentaje_credito, rate.Value, 25, has_codeudor)
            else:
                values_25 = None
            if date_30:
                values_30 = calculate_simulate_values(total_uf, porcentaje_credito, rate.Value, 30, has_codeudor)
            else:
                values_30 = None

            context_dict = {
                'reserva': instance,
                'cliente': cliente,
                'inmuebles_a_reservar': reserva_inmuebles,
                'proyecto': proyecto,
                'uf': valor_uf_actual(),
                'gestion': constants.COMPANY_NAME[0],
                'total_uf': total_uf,
                'total_credito': instance.PaymentInstitucionFinanciera,
                'porcentaje_credito': porcentaje_credito,
                'porcentaje_ahorro_plus': porcentaje_ahorro_plus,
                'ahorro_plus': instance.AhorroPlus,
                'rate': rate.Value,
                'values_8': values_8,
                'values_10': values_10,
                'values_15': values_15,
                'values_20': values_20,
                'values_25': values_25,
                'values_30': values_30,
                'tamaño_letra': 100,
            }

            simulador_pdf = render_create_simulador_to_pdf(context_dict)
            filename = "%s_SDC_%s.pdf" % (instance.Folio, cliente)
            simulador_pdf_generated = ContentFile(simulador_pdf)
            simulador_pdf_generated.name = filename
        else:
            ficha_pdf_generated = None
            simulador_pdf_generated = None

        documents_venta = DocumentVenta.objects.get(Folio=instance.Folio)
        documents_venta.DocumentOferta = oferta_pdf_generated
        documents_venta.DocumentFichaPreAprobacion = ficha_pdf_generated
        documents_venta.DocumentSimulador = simulador_pdf_generated
        documents_venta.save()

        instance.save()

        return instance


class SendControlReservaSerializer(serializers.ModelSerializer):
    ReservaState = serializers.CharField(
        source='ReservaStateID.Name'
    )

    class Meta:
        model = Reserva
        fields = ('ReservaState',)

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        if instance.ReservaStateID.Name == constants.RESERVA_STATE[1]:
            raise CustomValidation(
                "Reserva ya ha sido mandada a control",
                status_code=status.HTTP_409_CONFLICT)

        reserva_state = ReservaState.objects.get(
            Name=constants.RESERVA_STATE[1])

        # Registro en historial de ventas
        venta_log_type = VentaLogType.objects.get(
            Name=constants.VENTA_LOG_TYPE[1])

        VentaLog.objects.create(
            VentaID=instance.ReservaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
        )

        # Creacion de notificaciones
        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])
        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=jefe_proyecto_type)

        asistente_comercial_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[3])
        asistente_comercial = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=asistente_comercial_type)

        crear_notificacion_reserva_pendiente_control(
            instance, jefe_proyecto, asistente_comercial)

        instance.ReservaStateID = reserva_state
        instance.save()

        return instance


class ControlReservaSerializer(serializers.ModelSerializer):
    ReservaState = serializers.CharField(
        source='ReservaStateID.Name',
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
        model = Reserva
        fields = ('ReservaID', 'ReservaState',
                  'Resolution', 'Comment')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        comment = validated_data.get('comment', "")
        resolution = validated_data.pop('Resolution')

        if resolution:
            if instance.ReservaStateID.Name == constants.RESERVA_STATE[2]:
                raise CustomValidation(
                    "Reserva ya ha sido aprobada",
                    status_code=status.HTTP_409_CONFLICT)

            if instance.ReservaStateID.Name == constants.RESERVA_STATE[0]:
                raise CustomValidation(
                    "Reserva debe estar en estado pendiente control",
                    status_code=status.HTTP_409_CONFLICT)

            reserva_state = ReservaState.objects.get(
                Name=constants.RESERVA_STATE[2])
            venta_log_type = VentaLogType.objects.get(
                Name=constants.VENTA_LOG_TYPE[2])

            VentaLog.objects.create(
                VentaID=instance.ReservaID,
                Folio=instance.Folio,
                UserID=current_user,
                ClienteID=instance.ClienteID,
                ProyectoID=instance.ProyectoID,
                VentaLogTypeID=venta_log_type,
                Comment=comment,
            )

            eliminar_notificacion_reserva_pendiente_control(instance)
            ofertas.create_oferta(instance.ProyectoID, instance.ClienteID, instance.VendedorID, instance.CodeudorID,
                                  instance.EmpresaCompradoraID, instance.Folio, instance.CotizacionTypeID,
                                  instance.ContactMethodTypeID,
                                  instance.PaymentFirmaPromesa, instance.PaymentFirmaEscritura,
                                  instance.PaymentInstitucionFinanciera, instance.AhorroPlus, instance.PayTypeID,
                                  instance.DateFirmaPromesa,
                                  instance.ValueProductoFinanciero, current_user)
        else:
            if instance.ReservaStateID.Name == constants.RESERVA_STATE[2]:
                raise CustomValidation(
                    "Reserva ya ha sido aprobada, no se puede rechazar",
                    status_code=status.HTTP_409_CONFLICT)

            reserva_state = ReservaState.objects.get(
                Name=constants.RESERVA_STATE[3])
            venta_log_type = VentaLogType.objects.get(
                Name=constants.VENTA_LOG_TYPE[3])

            VentaLog.objects.create(
                VentaID=instance.ReservaID,
                Folio=instance.Folio,
                UserID=current_user,
                ClienteID=instance.ClienteID,
                ProyectoID=instance.ProyectoID,
                VentaLogTypeID=venta_log_type,
                Comment=comment,
            )

            # Crear/Eliminar notificaciones
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

            eliminar_notificacion_reserva_pendiente_control(instance)
            eliminar_notificacion_reserva_modificada_pendiente_control(instance)
            crear_notificacion_reserva_rechazada(
                instance, jefe_proyecto, vendedor)

        instance.ReservaStateID = reserva_state
        instance.save()

        return instance


class CancelReservaSerializer(serializers.ModelSerializer):
    ReservaState = serializers.CharField(
        source='ReservaStateID.Name'
    )

    Comment = serializers.CharField(
        write_only=True,
        allow_blank=True
    )

    class Meta:
        model = Reserva
        fields = ('ReservaState', 'Comment')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        if instance.ReservaStateID.Name == constants.RESERVA_STATE[4]:
            raise CustomValidation(
                "Reserva ya está cancelada",
                status_code=status.HTTP_409_CONFLICT)

        if instance.ReservaStateID.Name == constants.RESERVA_STATE[2]:
            raise CustomValidation(
                "Reserva en estado oferta no se puede cancelar",
                status_code=status.HTTP_409_CONFLICT)

        comment = validated_data.pop('Comment')

        reserva_state = ReservaState.objects.get(
            Name=constants.RESERVA_STATE[4])

        # Registro en historial de ventas
        venta_log_type = VentaLogType.objects.get(
            Name=constants.VENTA_LOG_TYPE[4])

        VentaLog.objects.create(
            VentaID=instance.ReservaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment
        )

        # Volver inmuebles asociados a estado disponible
        reserva_inmuebles = ReservaInmueble.objects.filter(ReservaID=instance)
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

        # Usuarios
        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=jefe_proyecto_type)

        vendedor = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID, UserProyectoTypeID=vendedor_type)

        asistente_comercial = UserProyecto.objects.filter(
            ProyectoID=instance.ProyectoID,
            UserProyectoTypeID=asistente_comercial_type)

        eliminar_notificaciones_reserva(instance)
        crear_notificacion_reserva_cancelada(
            instance, jefe_proyecto, vendedor, asistente_comercial)

        instance.ReservaStateID = reserva_state
        instance.save()

        return instance


class UploadDocumentsReservaSerializer(serializers.ModelSerializer):
    Folio = serializers.CharField(
        write_only=True
    )

    DocumentCotizacion = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentOfertaFirmada = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    '''
    DocumentOferta = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentFichaPreAprobacion = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentSimulador = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    '''
    DocumentCertificadoMatrimonio = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentConstitucionSociedad = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentPagoGarantia = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentFotocopiaCarnet = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentPreApprobation = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentLiquidacion1 = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentLiquidacion2 = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentLiquidacion3 = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCotizacionAFP = serializers.FileField(
        allow_empty_file=True,
        required=False
    )

    DocumentCertificadoSociedad = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCarpetaTributaria = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentBalancesTimbrados = serializers.FileField(
        allow_empty_file=True,
        required=False
    )

    Document6IVA = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    Document2DAI = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentTituloProfesional = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentAcredittacionAhorros = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentAcredittacionDeudas = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    # Coduedor
    DocumentCodeudorFirmadoCheques = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorFichaPreAprobacion = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorSimulador = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorCotizacion = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorCertificadoMatrimonio = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorFirmadoSimulador = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorConstitucionSociedad = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorCertificadoSociedad = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorCarpetaTributaria = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorBalancesTimbrados = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    Document6IVACodeudor = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    Document2DAICodeudor = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorTituloProfesional = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorAcredittacionAhorros = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorAcredittacionDeudas = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorFotocopiaCarnet = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorLiquidacion1 = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorLiquidacion2 = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentCodeudorLiquidacion3 = serializers.FileField(
        allow_empty_file=True,
        required=False
    )

    class Meta:
        model = Reserva
        fields = (
            'Folio',
            'DocumentOfertaFirmada',
            'DocumentCotizacion',
            'DocumentCertificadoMatrimonio',
            'DocumentConstitucionSociedad',
            'DocumentPagoGarantia',
            'DocumentFotocopiaCarnet',
            'DocumentPreApprobation',
            'DocumentLiquidacion1',
            'DocumentLiquidacion2',
            'DocumentLiquidacion3',
            'DocumentCotizacionAFP',
            'DocumentCertificadoSociedad',
            'DocumentCarpetaTributaria',
            'DocumentBalancesTimbrados',
            'Document6IVA',
            'Document2DAI',
            'DocumentTituloProfesional',
            'DocumentAcredittacionAhorros',
            'DocumentAcredittacionDeudas',
            'DocumentCodeudorFirmadoCheques',
            'DocumentCodeudorFichaPreAprobacion',
            'DocumentCodeudorSimulador',
            'DocumentCodeudorCotizacion',
            'DocumentCodeudorCertificadoMatrimonio',
            'DocumentCodeudorFirmadoSimulador',
            'DocumentCodeudorConstitucionSociedad',
            'DocumentCodeudorCertificadoSociedad',
            'DocumentCodeudorCarpetaTributaria',
            'DocumentCodeudorBalancesTimbrados',
            'Document6IVACodeudor',
            'Document2DAICodeudor',
            'DocumentCodeudorTituloProfesional',
            'DocumentCodeudorAcredittacionAhorros',
            'DocumentCodeudorAcredittacionDeudas',
            'DocumentCodeudorFotocopiaCarnet',
            'DocumentCodeudorLiquidacion1',
            'DocumentCodeudorLiquidacion2',
            'DocumentCodeudorLiquidacion3',
            )

    def create(self, validated_data):
        folio = validated_data['Folio']

        documents, aux = DocumentVenta.objects.get_or_create(Folio=folio)  # noqa

        if 'DocumentCotizacion' in validated_data:
            documents.DocumentCotizacion = validated_data['DocumentCotizacion']
        '''   
        if 'DocumentOferta' in validated_data:
            documents.DocumentOferta = validated_data['DocumentOferta']
        if 'DocumentFichaPreAprobacion' in validated_data:
            documents.DocumentFichaPreAprobacion = validated_data['DocumentFichaPreAprobacion']
        if 'DocumentSimulador' in validated_data:
            documents.DocumentSimulador = validated_data['DocumentSimulador']
        '''
        if 'DocumentOfertaFirmada' in validated_data:
            documents.DocumentOfertaFirmada = validated_data['DocumentOfertaFirmada']

        if 'DocumentCertificadoMatrimonio' in validated_data:
            documents.DocumentCertificadoMatrimonio = validated_data['DocumentCertificadoMatrimonio']
        if 'DocumentConstitucionSociedad' in validated_data:
            documents.DocumentConstitucionSociedad = validated_data['DocumentConstitucionSociedad']
        if 'DocumentPagoGarantia' in validated_data:
            documents.DocumentPagoGarantia = validated_data['DocumentPagoGarantia']
        if 'DocumentFotocopiaCarnet' in validated_data:
            documents.DocumentFotocopiaCarnet = validated_data['DocumentFotocopiaCarnet']
        if 'DocumentPreApprobation' in validated_data:
            documents.DocumentPreApprobation = validated_data['DocumentPreApprobation']
        if 'DocumentLiquidacion1' in validated_data:
            documents.DocumentLiquidacion1 = validated_data['DocumentLiquidacion1']
        if 'DocumentLiquidacion2' in validated_data:
            documents.DocumentLiquidacion2 = validated_data['DocumentLiquidacion2']
        if 'DocumentLiquidacion3' in validated_data:
            documents.DocumentLiquidacion3 = validated_data['DocumentLiquidacion3']
        if 'DocumentCotizacionAFP' in validated_data:
            documents.DocumentCotizacionAFP = validated_data['DocumentCotizacionAFP']

        if 'DocumentCertificadoSociedad' in validated_data:
            documents.DocumentCertificadoSociedad = validated_data['DocumentCertificadoSociedad']
        if 'DocumentCarpetaTributaria' in validated_data:
            documents.DocumentCarpetaTributaria = validated_data['DocumentCarpetaTributaria']
        if 'DocumentBalancesTimbrados' in validated_data:
            documents.DocumentBalancesTimbrados = validated_data['DocumentBalancesTimbrados']
        if 'Document6IVA' in validated_data:
            documents.Document6IVA = validated_data['Document6IVA']
        if 'Document2DAI' in validated_data:
            documents.Document2DAI = validated_data['Document2DAI']
        if 'DocumentTituloProfesional' in validated_data:
            documents.DocumentTituloProfesional = validated_data['DocumentTituloProfesional']
        if 'DocumentAcredittacionAhorros' in validated_data:
            documents.DocumentAcredittacionAhorros = validated_data['DocumentAcredittacionAhorros']
        if 'DocumentAcredittacionDeudas' in validated_data:
            documents.DocumentAcredittacionDeudas = validated_data['DocumentAcredittacionDeudas']
        
        #Codeudor
        if 'DocumentCodeudorFirmadoCheques' in validated_data:
            documents.DocumentCodeudorFirmadoCheques = validated_data['DocumentCodeudorFirmadoCheques']
        if 'DocumentCodeudorFichaPreAprobacion' in validated_data:
            documents.DocumentCodeudorFichaPreAprobacion = validated_data['DocumentCodeudorFichaPreAprobacion']
        if 'DocumentCodeudorSimulador' in validated_data:
            documents.DocumentCodeudorSimulador = validated_data['DocumentCodeudorSimulador']
        if 'DocumentCodeudorCotizacion' in validated_data:
            documents.DocumentCodeudorCotizacion = validated_data['DocumentCodeudorCotizacion']
        if 'DocumentCodeudorCertificadoMatrimonio' in validated_data:
            documents.DocumentCodeudorCertificadoMatrimonio = validated_data['DocumentCodeudorCertificadoMatrimonio']
        if 'DocumentCodeudorFirmadoSimulador' in validated_data:
            documents.DocumentCodeudorFirmadoSimulador = validated_data['DocumentCodeudorFirmadoSimulador']
        if 'DocumentCodeudorConstitucionSociedad' in validated_data:
            documents.DocumentCodeudorConstitucionSociedad = validated_data['DocumentCodeudorConstitucionSociedad']
        if 'DocumentCodeudorCertificadoSociedad' in validated_data:
            documents.DocumentCodeudorCertificadoSociedad = validated_data['DocumentCodeudorCertificadoSociedad']
        if 'DocumentCodeudorCarpetaTributaria' in validated_data:
            documents.DocumentCodeudorCarpetaTributaria = validated_data['DocumentCodeudorCarpetaTributaria']
        if 'DocumentCodeudorBalancesTimbrados' in validated_data:
            documents.DocumentCodeudorBalancesTimbrados = validated_data['DocumentCodeudorBalancesTimbrados']
        if 'Document6IVACodeudor' in validated_data:
            documents.Document6IVACodeudor = validated_data['Document6IVACodeudor']
        if 'Document2DAICodeudor' in validated_data:
            documents.Document2DAICodeudor = validated_data['Document2DAICodeudor']
        if 'DocumentCodeudorTituloProfesional' in validated_data:
            documents.DocumentCodeudorTituloProfesional = validated_data['DocumentCodeudorTituloProfesional']
        if 'DocumentCodeudorAcredittacionAhorros' in validated_data:
            documents.DocumentCodeudorAcredittacionAhorros = validated_data['DocumentCodeudorAcredittacionAhorros']
        if 'DocumentCodeudorAcredittacionDeudas' in validated_data:
            documents.DocumentCodeudorAcredittacionDeudas = validated_data['DocumentCodeudorAcredittacionDeudas']
        if 'DocumentCodeudorFotocopiaCarnet' in validated_data:
            documents.DocumentCodeudorFotocopiaCarnet = validated_data['DocumentCodeudorFotocopiaCarnet']
        if 'DocumentCodeudorLiquidacion1' in validated_data:
            documents.DocumentCodeudorLiquidacion1 = validated_data['DocumentCodeudorLiquidacion1']
        if 'DocumentCodeudorLiquidacion2' in validated_data:
            documents.DocumentCodeudorLiquidacion2 = validated_data['DocumentCodeudorLiquidacion2']
        if 'DocumentCodeudorLiquidacion3' in validated_data:
            documents.DocumentCodeudorLiquidacion3 = validated_data['DocumentCodeudorLiquidacion3']
                
        documents.save()

        return documents

class DownloadPreApprobationSerializer(serializers.ModelSerializer):
    ReservaID = serializers.UUIDField(
        write_only=True
    )
    LetterSize = serializers.IntegerField(
        write_only=True
    )

    class Meta:
        model = Reserva
        fields = ('ReservaID', 'LetterSize')
