from django.db import transaction
from django.core.mail import send_mail
from rest_framework import serializers, status

from common import constants
from common.services import return_current_user, get_or_none
from common.validations import CustomValidation
from empresas_and_proyectos.models.inmuebles import Inmueble
from empresas_and_proyectos.models.inmuebles_restrictions import InmuebleInmueble
from empresas_and_proyectos.models.proyectos import Proyecto
from empresas_and_proyectos.models.instituciones_financieras import (
    InstitucionFinanciera)
from empresas_and_proyectos.serializers.inmuebles import ListOrientationSerializer
from empresas_and_proyectos.serializers.proyectos import RestrictionSerializer
from users.models import User
from users.serializers.users import UserProfileSerializer
from ventas.models.clientes import (
    Cliente,
    ClienteProyecto)
from ventas.models.cotizaciones import (
    Cotizacion,
    CotizacionInmueble,
    CotizacionType,
    CotizacionState)
from ventas.models.counter_folios import CounterFolio
from ventas.models.finding_contact import (
    FindingType,
    ContactMethodType)
from ventas.models.payment_forms import Cuota, PayType
from ventas.models.ventas_logs import (
    VentaLogType,
    VentaLog)
from ventas.serializers.clientes import (
    ListClienteSerializer, 
    CreateClienteContactInfoSerializer)
from .cuotas import (
    ListCuotaSerializer,
    CreateCuotaSerializer)
from .empresas_compradoras import (EmpresaCompradoraSerializer)
from ventas.models.empresas_compradoras import EmpresaCompradora
from sgi_web_back_project import settings

class CotizacionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CotizacionType
        fields = ('CotizacionTypeID', 'Name')


class ListCotizacionesInmueblesSerializer(serializers.ModelSerializer):
    InmuebleID = serializers.CharField(
        source='InmuebleID.InmuebleID'
    )

    InmuebleType = serializers.CharField(
        source='InmuebleID.InmuebleTypeID.Name'
    )
    Number = serializers.IntegerField(
        source='InmuebleID.Number'
    )
    Restrictions = serializers.SerializerMethodField('get_restrictions')

    class Meta:
        model = CotizacionInmueble
        fields = ('InmuebleID', 'InmuebleType', 'Number', 'Restrictions')

    def get_restrictions(self, obj):
        restrictions = InmuebleInmueble.objects.filter(InmuebleAID=obj.InmuebleID).select_related('InmuebleAID',
                                                                                                  'InmuebleBID',
                                                                                                  'InmuebleInmuebleTypeID')
        data = [RestrictionSerializer(restriction).to_dict() for restriction in restrictions]
        return data


class ListCotizacionInmuebleSerializer(serializers.ModelSerializer):
    InmuebleID = serializers.CharField(
        source='InmuebleID.InmuebleID'
    )
    InmuebleType = serializers.CharField(
        source='InmuebleID.InmuebleTypeID.Name'
    )
    Number = serializers.IntegerField(
        source='InmuebleID.Number'
    )
    Floor = serializers.IntegerField(
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
        model = CotizacionInmueble
        fields = ('InmuebleID', 'InmuebleType',
                  'Number', 'Floor', 'Tipologia',
                  'Price', 'BedroomsQuantity',
                  'BathroomQuantity', 'Orientation', 'Discount', 'Restrictions')

    def get_restrictions(self, obj):
        restrictions = InmuebleInmueble.objects.filter(InmuebleAID=obj.InmuebleID).select_related('InmuebleAID',
                                                                                                  'InmuebleBID',
                                                                                                  'InmuebleInmuebleTypeID')
        data = [RestrictionSerializer(restriction).to_dict() for restriction in restrictions]
        return data


class CotizacionSerializer(serializers.ModelSerializer):
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )
    Proyecto = serializers.CharField(
        source='ProyectoID.Name'
    )
    ClienteID = serializers.CharField(
        source='ClienteID.UserID'
    )
    Cliente = ListClienteSerializer(
        source='ClienteID'
    )
    CotizadorID = serializers.CharField(
        source='CotizadorID.UserID'
    )
    CotizadorName = serializers.CharField(
        source='CotizadorID.Name'
    )
    CotizadorLastNames = serializers.CharField(
        source='CotizadorID.LastNames'
    )
    CotizadorRut = serializers.CharField(
        source='CotizadorID.Rut'
    )
    CotizacionState = serializers.CharField(
        source='CotizacionStateID.Name'
    )
    CotizacionType = serializers.CharField(
        source='CotizacionTypeID.Name'
    )
    ContactMethodType = serializers.CharField(
        source='ContactMethodTypeID.Name'
    )
    ContactMethodTypeID = serializers.CharField(
        source='ContactMethodTypeID.ContactMethodTypeID'
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
    Subsidio = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    ) 
    Libreta = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    InstitucionFinanciera = serializers.UUIDField(
        source='InstitucionFinanciera.InstitucionFinancieraID'
    )
    Cuotas = ListCuotaSerializer(
        source='CuotaID', many=True
    )
    Inmuebles = serializers.SerializerMethodField('get_inmuebles')
    Date = serializers.SerializerMethodField('get_date')
    DateFirmaPromesa = serializers.SerializerMethodField('get_date_firma_promesa')
    PaymentCuotas = serializers.SerializerMethodField('get_total_cuotas')
    Vendedor = UserProfileSerializer()
    VendedorID = serializers.UUIDField(
        source='Vendedor.UserID'
    )
    PayType = serializers.UUIDField(
        source='PayType.PayTypeID'
    )	
    EmpresaCompradora = serializers.SerializerMethodField('get_empresa_compradora')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ProyectoID',
            'ClienteID',
            'CotizadorID',
            'CotizacionStateID',
            'CotizacionTypeID',
            'ContactMethodTypeID')
        queryset = queryset.prefetch_related('CuotaID', 'InmuebleID')
        return queryset

    class Meta:
        model = Cotizacion
        fields = (
            'CotizacionID',
            'ProyectoID',
            'Proyecto',
            'ClienteID',
            'Cliente',
            'CotizadorID',
            'CotizadorName',
            'CotizadorLastNames',
            'CotizadorRut',
            'Date',
            'DateFirmaPromesa',
            'Folio',
            'CotizacionState',
            'CotizacionType',
            'ContactMethodType',
            'ContactMethodTypeID',
            'PaymentFirmaPromesa',
            'PaymentFirmaEscritura',
            'PaymentInstitucionFinanciera',
            'PaymentCuotas',
            'AhorroPlus',
            'Subsidio',
            'Libreta',
            'InstitucionFinanciera',
            'IsNotInvestment',
            'Cuotas',
            'Inmuebles',
            'Vendedor',
            'VendedorID',
            'PayType',
            'EmpresaCompradora'
        )

    def get_inmuebles(self, obj):
        inmuebles_cotizacion = CotizacionInmueble.objects.filter(
            CotizacionID=obj)
        serializer = ListCotizacionInmuebleSerializer(
            instance=inmuebles_cotizacion, many=True)
        return serializer.data

    def get_date(self, obj):
        try:
            return obj.Date.strftime("%Y-%m-%d")
        except AttributeError:
            return ""

    def get_date_firma_promesa(self, obj):
        try:
            return obj.DateFirmaPromesa.strftime("%Y-%m-%d")
        except AttributeError:
            return ""

    def get_total_cuotas(self, obj):
        cuotas = obj.CuotaID.all()
        total = 0
        for cuota in cuotas:
            total += cuota.Amount
        return total
        
    def get_empresa_compradora(self, obj):
        empresa_compradora = EmpresaCompradora.objects.filter(
            ClienteID=obj.ClienteID)
        if empresa_compradora.exists():
            return EmpresaCompradoraSerializer(instance=empresa_compradora[0]).data
        return None    


class ListCotizacionSerializer(serializers.ModelSerializer):
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )
    Cliente = ListClienteSerializer(
        source='ClienteID'
    )
    ClienteID = serializers.UUIDField(
        source='ClienteID.UserID'
    )
    CotizacionState = serializers.CharField(
        source='CotizacionStateID.Name'
    )
    CotizacionType = serializers.CharField(
        source='CotizacionTypeID.Name'
    )
    Vendedor = UserProfileSerializer()
    VendedorID = serializers.UUIDField(
        source='Vendedor.UserID'
    )
    Inmuebles = serializers.SerializerMethodField('get_inmuebles')
    PayType = serializers.CharField(
        source='PayType.Name'
    )

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ProyectoID',
            'ClienteID',
            'CotizacionStateID',
            'CotizacionTypeID',
        )
        queryset = queryset.prefetch_related('CuotaID', 'InmuebleID', 'ProyectoID')
        return queryset

    class Meta:
        model = Cotizacion
        fields = (
            'ProyectoID',
            'CotizacionID',
            'Cliente',
            'ClienteID',
            'Folio',
            'CotizacionState',
            'CotizacionType',
            'Inmuebles',
            'Vendedor',
            'VendedorID',
            'PayType',
            'Date',
        )

    def get_inmuebles(self, obj):
        inmuebles_cotizacion = CotizacionInmueble.objects.filter(CotizacionID=obj).prefetch_related(
            'InmuebleID__InmuebleRestrict')
        serializer = ListCotizacionesInmueblesSerializer(
            instance=inmuebles_cotizacion, many=True)
        return serializer.data


class DownloadCotizacionSerializer(serializers.ModelSerializer):
    CotizacionID = serializers.UUIDField(
        write_only=True
    )
    LetterSize = serializers.IntegerField(
        write_only=True
    )

    class Meta:
        model = Cotizacion
        fields = ('CotizacionID', 'LetterSize')


class CreateCotizacionInmuebleSerializer(serializers.ModelSerializer):
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
        model = CotizacionInmueble
        fields = ('InmuebleID', 'Discount')


class CreateClienteCotizacionSerializer(serializers.ModelSerializer):
    Rut = serializers.CharField()
    Address = serializers.CharField(
        allow_blank=True,
        required=False
    )
    Contact = CreateClienteContactInfoSerializer(
        source='ContactInfo',
        many=True
    )
    Nationality = serializers.CharField(
        required=False,
        allow_blank=True
    )
    Genre = serializers.CharField(
        required=False,
        allow_blank=True
    )
    CivilStatus = serializers.CharField(
        required=False,
        allow_blank=True
    )
    Ocupation = serializers.CharField(
        allow_blank=True,
        required=False
    )
    Position = serializers.CharField(
        required=False,
        allow_blank=True
    )
    Antiquity = serializers.CharField(
        required=False,
        allow_blank=True
    )
    ContractMarriageType = serializers.CharField(
        required=False,
        allow_blank=True
    )
    ComunaID = serializers.CharField(
        write_only=True,
        allow_blank=True,
        required=False
    )
    BirthDate = serializers.DateField(
        write_only=True,
        allow_null=True
    )
    FindingTypeID = serializers.UUIDField(
        write_only=True,
        allow_null=True,
        required=False
    )
    Extra = serializers.JSONField()

    class Meta:
        model = Cliente
        fields = ('Name', 'LastNames', 'Rut',
                  'Address', 'ComunaID', 'Contact',
                  'Nationality', 'Genre', 'BirthDate',
                  'CivilStatus', 'Ocupation', 'Position',
                  'Carga', 'Salary', 'TotalPatrimony',
                  'Antiquity', 'ContractMarriageType',
                  'IsDefinitiveResidence', 'FindingTypeID',
                  'IsCompany', 'Extra')


class CreateCotizacionSerializer(serializers.ModelSerializer):
    ProyectoID = serializers.UUIDField(
        write_only=True
    )
    Cliente = serializers.JSONField(
        source='ClienteID',
        allow_null=True
    )
    Cuotas = CreateCuotaSerializer(
        source='CuotaID',
        many=True
    )
    Inmuebles = CreateCotizacionInmuebleSerializer(
        source='InmuebleID',
        many=True
    )
    CotizacionType = serializers.CharField(
        write_only=True
    )
    ContactMethodTypeID = serializers.UUIDField(
        write_only=True,
        allow_null=True,
        required=False
    )
    DateFirmaPromesa = serializers.DateTimeField(
        write_only=True,
        allow_null=True,
        required=False
    )
    PaymentFirmaPromesa = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True
    )
    PaymentFirmaEscritura = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True
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
        allow_null=True
    ) 
    Libreta = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True
    )
    InstitucionFinanciera = serializers.UUIDField(
        allow_null=True
    )
    VendedorID = serializers.UUIDField(
        allow_null=True
    )

    PayType = serializers.UUIDField()

    class Meta:
        model = Cotizacion
        fields = (
            'ProyectoID',
            'Cliente',
            'Cuotas',
            'Inmuebles',
            'CotizacionType',
            'ContactMethodTypeID',
            'DateFirmaPromesa',
            'PaymentFirmaPromesa',
            'PaymentFirmaEscritura',
            'PaymentInstitucionFinanciera',
            'AhorroPlus',
            'Subsidio',
            'Libreta',
            'InstitucionFinanciera',
            'IsNotInvestment',
            'VendedorID',
            'PayType'
        )

    def create(self, validated_data):
        current_user = return_current_user(self)
		
        cuotas_data = validated_data.pop('CuotaID')
        inmuebles_data = validated_data.pop('InmuebleID')

        total = 0
        total_uf = 0
        total_cuotas = 0

        proyecto = Proyecto.objects.get(
            ProyectoID=validated_data['ProyectoID'])
        cotizacion_type = CotizacionType.objects.get(
            Name=validated_data['CotizacionType'])
        cotizacion_state = CotizacionState.objects.get(
            Name=constants.COTIZATION_STATE[0])

        with transaction.atomic():
            counter_folio = CounterFolio.objects.get(ProyectoID=proyecto)
            counter_folio.Count += 1
            counter_folio.save()
            counter_folio.Count -= 1

        cliente_data = validated_data.pop('ClienteID')
        if not cliente_data.get('UserID'):
            raise CustomValidation(
                "ClienteID es requerido",
                status_code=status.HTTP_409_CONFLICT)
        cliente = Cliente.objects.get(UserID=cliente_data.get('UserID'))

        if cotizacion_type.Name == constants.COTIZATION_TYPE[0]:
            if not cliente_data.get('FindingTypeID'):
                raise CustomValidation(
                    "Cotización Presencial: ¿Como se entero del proyecto? obligatorio",
                    status_code=status.HTTP_409_CONFLICT)

            finding_type = FindingType.objects.get(
                FindingTypeID=cliente_data['FindingTypeID'])
        else:
            finding_type = get_or_none(FindingType, FindingTypeID=cliente_data['FindingTypeID']) if cliente_data.get('FindingTypeID') else False

        cliente_proyecto = ClienteProyecto.objects.filter(UserID=cliente, ProyectoID=proyecto)
        if cliente_proyecto.exists():
            for client in cliente_proyecto:
                if finding_type is not False:
                    client.FindingTypeID = finding_type
                client.save()
        else:
            if finding_type is False:
                finding_type = None
            ClienteProyecto.objects.create(
                UserID=cliente,
                ProyectoID=proyecto,
                FindingTypeID=finding_type,
            )

        if cotizacion_type.Name == constants.COTIZATION_TYPE[0]:
            if not validated_data.get('ContactMethodTypeID'):
                contact_method_type = ContactMethodType.objects.get(
                    Name=constants.CONTACT_METHOD_TYPE[3])
            else:
                contact_method_type = ContactMethodType.objects.get(
                    ContactMethodTypeID=validated_data['ContactMethodTypeID'])
        else:
            if not validated_data.get('ContactMethodTypeID'):
                raise CustomValidation(
                    "Cotización No presencial: Medio de contacto Cliente-Vendedor obligatorio",
                    status_code=status.HTTP_409_CONFLICT)
            else:
                contact_method_type = ContactMethodType.objects.get(
                    ContactMethodTypeID=validated_data['ContactMethodTypeID'])

        vendedor = get_or_none(User, UserID=validated_data['VendedorID'])
        paytype = get_or_none(PayType, PayTypeID=validated_data.get('PayType'))
        folio = proyecto.Symbol + str(counter_folio.Count)

        libretaBank=get_or_none(InstitucionFinanciera, InstitucionFinancieraID=validated_data.get('InstitucionFinanciera'))

        instance = Cotizacion.objects.create(
            ProyectoID=proyecto,
            ClienteID=cliente,
            Vendedor=vendedor,
            CotizadorID=current_user,
            Folio=folio,
            CotizacionStateID=cotizacion_state,
            CotizacionTypeID=cotizacion_type,
            ContactMethodTypeID=contact_method_type,
            PayType=paytype,
            IsNotInvestment=validated_data.get('IsNotInvestment', False),
            DateFirmaPromesa=validated_data['DateFirmaPromesa'],
            PaymentFirmaPromesa=validated_data['PaymentFirmaPromesa'],
            PaymentFirmaEscritura=validated_data['PaymentFirmaEscritura'],
            PaymentInstitucionFinanciera=validated_data['PaymentInstitucionFinanciera'],
            AhorroPlus=validated_data['AhorroPlus'],
            Subsidio=validated_data['Subsidio'],
            Libreta=validated_data['Libreta'],
            InstitucionFinanciera=libretaBank
        )
        for cuota_data in cuotas_data:
            cuota = Cuota.objects.create(
                Amount=cuota_data['Amount'],
                Date=cuota_data['Date'],
                Observacion=cuota_data.get('Observacion')
            )
            instance.CuotaID.add(cuota)

        cotizacion_inmuebles = list()

        for inmueble_data in inmuebles_data:
            inmueble = Inmueble.objects.get(
                InmuebleID=inmueble_data['InmuebleID']
            )
            if inmueble_data['Discount']:
                discount = inmueble_data['Discount']
            else:
                discount = None

            cotizacion_inmueble = CotizacionInmueble()
            cotizacion_inmueble.CotizacionID = instance
            cotizacion_inmueble.InmuebleID = inmueble
            cotizacion_inmueble.Discount = discount

            cotizacion_inmuebles.append(cotizacion_inmueble)

        CotizacionInmueble.objects.bulk_create(cotizacion_inmuebles)

        inmuebles_a_cotizar = CotizacionInmueble.objects.filter(
            CotizacionID=instance)

        for cotizacion_inmueble in inmuebles_a_cotizar:
            if cotizacion_inmueble.Discount:
                price_discount = (cotizacion_inmueble.InmuebleID.Price * cotizacion_inmueble.Discount / 100)
                price = cotizacion_inmueble.InmuebleID.Price - price_discount
                total_uf += price
            else:
                total_uf += cotizacion_inmueble.InmuebleID.Price
        
        if instance.CuotaID.all():
            for cuota in instance.CuotaID.all():
                total_cuotas += cuota.Amount
            total += total_cuotas

        if validated_data['PaymentFirmaPromesa']:
            total += validated_data['PaymentFirmaPromesa']

        total += 0 if not validated_data.get('PaymentFirmaEscritura') else validated_data['PaymentFirmaEscritura']

        if validated_data.get('PaymentInstitucionFinanciera'):
            total += validated_data['PaymentInstitucionFinanciera']
        
        # More discount    
        if validated_data.get('AhorroPlus'):
            total += validated_data['AhorroPlus']    

        '''
        Previene errores de precision recordando que hay calculos de
        operaciones punto flotante que se hacen con javascript en el FE
        y otras con Python en el BE
        '''
        
        # if not abs(total_uf - total) <= constants.DEFAULT_PRECISION:
        #     raise CustomValidation(
        #         "Monto por pagar debe ser igual a monto total a pagar",
        #         status_code=status.HTTP_409_CONFLICT)

        # Registro Bitacora de Ventas
        venta_log_type = VentaLogType.objects.get(
            Name=constants.VENTA_LOG_TYPE[16])

        VentaLog.objects.create(
            VentaID=instance.CotizacionID,
            Folio=folio,
            UserID=current_user,
            ClienteID=cliente,
            ProyectoID=proyecto,
            VentaLogTypeID=venta_log_type,
        )

        # send email to client        
        contact_emails = []
        for contact_info in cliente_data.get('Contact'):
            if contact_info.get('ContactInfoType') == 'Email':
                contact_emails.append(contact_info.get('Value'))
        
        # send_mail(message="To Clente",
        #           subject="creating new Cotizacion",
        #           from_email=settings.EMAIL_HOST_USER,
        #           recipient_list=contact_emails,
        #           html_message="message")

        # end sending email

        return instance


class ListCotizacionActionSerializer(serializers.ModelSerializer):
    ApprovedUserInfo = serializers.SerializerMethodField('get_user')
    Date = serializers.SerializerMethodField('get_date')
    SaleState = serializers.SerializerMethodField('get_state')
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )
    VentaID = serializers.CharField(
        source='CotizacionID'
    )

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'CotizacionStateID'
        )
        return queryset

    class Meta:
        model = Cotizacion
        fields = (
            'CotizacionID', 'ProyectoID',
            'Folio', 'SaleState', 'VentaID',
            'Date', 'ApprovedUserInfo'
        )

    def get_user(self, obj):
        venta_log = VentaLog.objects.filter(VentaID=obj.CotizacionID).order_by('-Date').first()
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
            return obj.CotizacionStateID.Name+" cotizacion"
        except AttributeError:
            return ""


class UserCotizacionActionSerializer(serializers.ModelSerializer):
    ApprovedUserInfo = serializers.SerializerMethodField('get_user')
    Date = serializers.SerializerMethodField('get_date')
    SaleState = serializers.SerializerMethodField('get_state')
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'CotizacionStateID'
        )
        return queryset

    class Meta:
        model = Cotizacion
        fields = (
            'CotizacionID', 'ProyectoID',
            'Folio', 'SaleState',
            'Date', 'ApprovedUserInfo'
        )

    def get_user(self, obj):
        venta_log = VentaLog.objects.filter(VentaID=obj.CotizacionID).order_by('-Date').first()
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
            return obj.CotizacionStateID.Name + " cotizacion"
        except AttributeError:
            return ""