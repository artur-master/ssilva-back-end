from rest_framework import serializers

from common.serializers.comunas import ComunaSerializer
from common.services import return_current_user, get_or_none
from common.validations import validate_rut_usuario, CustomValidation
from ventas.models.clientes import (
    Cliente,
    ClienteContactInfo,
    ClienteProyecto)
from ventas.models.cotizaciones import Cotizacion
from ventas.models.empleadores import Empleador
from ventas.snippets.clientes_serializers import save_cliente
from .empleadores import EmpleadorSerializer
from users.models import User
from rest_framework import status


class CreateClienteContactInfoSerializer(serializers.ModelSerializer):
    ContactInfoTypeID = serializers.UUIDField(
        write_only=True
    )
    ContactInfoType = serializers.CharField(
        source='ContactInfoTypeID',
        read_only=True
    )
    Value = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = ClienteContactInfo
        fields = ('ContactInfoTypeID', 'ContactInfoType', 'Value')


class ClienteContactInfoSerializer(serializers.ModelSerializer):
    ContactInfoTypeID = serializers.CharField(
        source='ContactInfoTypeID.ContactInfoTypeID'
    )
    ContactInfoType = serializers.CharField(
        source='ContactInfoTypeID.Name',
        read_only=True
    )

    class Meta:
        model = ClienteContactInfo
        fields = ('ContactInfoTypeID', 'ContactInfoType', 'Value')


class ClienteProyectoSerializer(serializers.ModelSerializer):
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID',
        read_only=True
    )
    Proyecto = serializers.CharField(
        source='ProyectoID.Name',
        read_only=True
    )
    FindingTypeID = serializers.CharField(
        source='FindingTypeID.FindingTypeID',
        read_only=True
    )
    FindingType = serializers.CharField(
        source='FindingTypeID.Name',
        read_only=True
    )

    class Meta:
        model = ClienteProyecto
        fields = ('ProyectoID', 'Proyecto', 'FindingTypeID', 'FindingType')


class ListClienteSerializer(serializers.ModelSerializer):
    ComunaID = serializers.CharField(source='ComunaID.ComunaID',
                                     read_only=True,
                                     allow_null=True)
    Comuna = ComunaSerializer(
        source='ComunaID',
        read_only=True,
        allow_null=True
    )
    Contact = serializers.SerializerMethodField()
    BirthDate = serializers.SerializerMethodField()
    ClienteProyecto = serializers.SerializerMethodField(
        'get_cliente_project')
    Empleador = serializers.SerializerMethodField('get_empleador_cliente')    
    def get_Contact(self, obj):
        query_set = ClienteContactInfo.objects.filter(UserID=obj)
        return [ClienteContactInfoSerializer(instance).data for instance in query_set]

    def get_BirthDate(self, obj):
        try:
            return obj.BirthDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_cliente_project(self, obj):
        cliente_project = ClienteProyecto.objects.filter(
            UserID=obj)
        serializer = ClienteProyectoSerializer(
            instance=cliente_project, many=True)
        return serializer.data
    def get_empleador_cliente(self, obj):
        empleador_cliente = Empleador.objects.filter(ClienteID=obj).order_by("-id")
        if empleador_cliente.exists():
            empleador_cliente = empleador_cliente[0]
            serializer = EmpleadorSerializer(
                instance=empleador_cliente)
            return serializer.data
        return None    
    
    class Meta:
        model = Cliente
        fields = ('UserID', 'Name', 'LastNames',
                  'Rut', 'ComunaID', 'Comuna', 'Address',
                  'Nationality', 'Genre', 'BirthDate',
                  'CivilStatus', 'Ocupation', 'Position',
                  'Carga', 'Salary', 'TotalPatrimony',
                  'Antiquity', 'ContractMarriageType',
                  'GiroEmpresa', 'ReprenetanteLegal',
                  'Extra', 'IsCompany', 'IsDefinitiveResidence', 'Contact','ClienteProyecto','Empleador')


class ClienteSerializer(serializers.ModelSerializer):
    Provincia = serializers.CharField(
        source='ComunaID.ProvinciaID.Name',
        read_only=True
    )
    Comuna = serializers.CharField(
        source='ComunaID.Name',
        read_only=True
    )
    ComunaID = serializers.CharField(
        source='ComunaID.ComunaID',
        read_only=True
    )
    Region = serializers.CharField(
        source='ComunaID.ProvinciaID.RegionID.Name',
        read_only=True
    )
    CreatorUserID = serializers.CharField(
        source='Creator.UserID',
        read_only=True
    )
    CreatorName = serializers.CharField(
        source='Creator.Name',
        read_only=True
    )
    CreatorLastNames = serializers.CharField(
        source='Creator.LastNames',
        read_only=True
    )
    CreatorRut = serializers.CharField(
        source='Creator.Rut',
        read_only=True
    )
    LastModifierUserID = serializers.CharField(
        source='LastModifier.UserID',
        read_only=True
    )
    LastModifierName = serializers.CharField(
        source='LastModifier.Name',
        read_only=True
    )
    LastModifierLastNames = serializers.CharField(
        source='LastModifier.LastNames',
        read_only=True
    )
    LastModifierRut = serializers.CharField(
        source='LastModifier.Rut',
        read_only=True
    )

    Empleador = serializers.SerializerMethodField('get_empleador_cliente')
    ClienteProyecto = serializers.SerializerMethodField(
        'get_cliente_proyectos')
    Contact = serializers.SerializerMethodField('get_cliente_contact_info')
    Cotizaciones = serializers.SerializerMethodField(
        'get_cliente_cotizaciones')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ComunaID',
            'Creator',
            'LastModifier')
        queryset = queryset.prefetch_related('ContactInfo', 'Proyecto')
        return queryset

    class Meta:
        model = Cliente
        fields = (
            'UserID',
            'Name',
            'LastNames',
            'Rut',
            'Nationality',
            'Genre',
            'BirthDate',
            'CivilStatus',
            'Ocupation',
            'Position',
            'Carga',
            'Salary',
            'TotalPatrimony',
            'ContractMarriageType',
            'Empleador',
            'Antiquity',
            'IsDefinitiveResidence',
            'Contact',
            'Address',
            'Provincia',
            'Comuna',
            'ComunaID',
            'Region',
            'ClienteProyecto',
            'CreationDate',
            'LastModificationDate',
            'CreatorUserID',
            'CreatorName',
            'CreatorLastNames',
            'CreatorRut',
            'LastModifierUserID',
            'LastModifierName',
            'LastModifierLastNames',
            'LastModifierRut',
            'IsCompany',
            'Extra',
            'Cotizaciones',
            'GiroEmpresa', 
            'ReprenetanteLegal')

    def get_empleador_cliente(self, obj):
        empleador_cliente = Empleador.objects.filter(ClienteID=obj).order_by("-id")
        if empleador_cliente.exists():
            empleador_cliente = empleador_cliente[0]
            serializer = EmpleadorSerializer(
                instance=empleador_cliente)
            return serializer.data
        return None

    def get_cliente_contact_info(self, obj):
        clientes_contact_info = ClienteContactInfo.objects.filter(
            UserID=obj)
        serializer = ClienteContactInfoSerializer(
            instance=clientes_contact_info, many=True)
        return serializer.data

    def get_cliente_proyectos(self, obj):
        cliente_proyecto = ClienteProyecto.objects.filter(
            UserID=obj)
        serializer = ClienteProyectoSerializer(
            instance=cliente_proyecto, many=True)
        return serializer.data

    def get_cliente_cotizaciones(self, obj):
        from ventas.serializers.cotizaciones import CotizacionSerializer
        cliente_cotizacion = Cotizacion.objects.filter(
            ClienteID=obj)
        serializer = CotizacionSerializer(
            instance=cliente_cotizacion, many=True)
        return serializer.data


class CreateClienteSerializer(serializers.ModelSerializer):
    Rut = serializers.CharField(
        validators=[validate_rut_usuario]
    )
    Contact = CreateClienteContactInfoSerializer(
        source='ContactInfo',
        many=True
    )
    Address = serializers.CharField(
        allow_blank=True
    )
    ComunaID = serializers.CharField(
        write_only=True,
        allow_blank=True
    )

    class Meta:
        model = Cliente
        fields = ('Name', 'LastNames', 'Rut',
                  'Address', 'ComunaID', 'Contact',
                  'Nationality', 'Genre', 'BirthDate',
                  'CivilStatus', 'Ocupation', 'Position',
                  'Carga', 'Salary', 'TotalPatrimony',
                  'Antiquity', 'ContractMarriageType',
                  'IsDefinitiveResidence', 'IsCompany',
                  'GiroEmpresa', 'ReprenetanteLegal',
                  'Extra')

    def create(self, validated_data):
        current_user = return_current_user(self)
        
        instance = Cliente()
        save_cliente(validated_data, instance, current_user)
        return instance


class UpdateClienteSerializer(serializers.ModelSerializer):
    Contact = CreateClienteContactInfoSerializer(
        source='ContactInfo',
        many=True,
        required=False
    )
    Address = serializers.CharField(
        allow_blank=True,
        required=False
    )
    ComunaID = serializers.CharField(
        write_only=True,
        allow_blank=True,
        required=False
    )

    class Meta:
        model = Cliente
        fields = ('Rut', 'Name', 'LastNames',
                  'Address', 'ComunaID', 'Contact',
                  'Nationality', 'Genre', 'BirthDate',
                  'CivilStatus', 'Ocupation', 'Position',
                  'Carga', 'Salary', 'TotalPatrimony',
                  'Antiquity', 'ContractMarriageType',
                  'IsDefinitiveResidence','IsCompany',
                  'GiroEmpresa', 'ReprenetanteLegal',
                  'Extra')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        rut = validated_data['Rut']
        if instance.Rut != rut:
            user = User.objects.filter(Rut=rut)
            if user.exists():
                raise CustomValidation(
                    'Rut ingresado ya existe en el sistema',
                    status_code=status.HTTP_409_CONFLICT)
        
        save_cliente(validated_data, instance, current_user)
        return instance
