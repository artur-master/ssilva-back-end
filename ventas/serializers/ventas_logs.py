from users.serializers.users import UserProfileSerializer
from ventas.models.ventas_logs import VentaLog
from rest_framework import serializers

from ventas.serializers.clientes import ClienteSerializer


class VentaLogClienteSerializer(serializers.ModelSerializer):
    VendedorName = serializers.CharField(
        source='UserID.Name'
    )
    VendedorLastNames = serializers.CharField(
        source='UserID.LastNames'
    )
    VendedorRut = serializers.CharField(
        source='UserID.Rut'
    )
    VentaLogType = serializers.CharField(
        source='VentaLogTypeID.Name'
    )
    Date = serializers.SerializerMethodField('get_date')
    Comment = serializers.SerializerMethodField('get_comment')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'UserID', 'VentaLogTypeID')
        return queryset

    class Meta:
        model = VentaLog
        fields = ('VentaLogID', 'VendedorName', 'VendedorLastNames',
                  'VendedorRut', 'VentaLogType', 'Date', 'Comment')

    def get_date(self, obj):
        try:
            return obj.Date.strftime("%Y-%m-%d")
        except AttributeError:
            return ""

    def get_comment(self, obj):
        if obj.Comment:
            return obj.Comment
        return ""


class VentaLogVendedorSerializer(serializers.ModelSerializer):
    ClienteName = serializers.CharField(
        source='ClienteID.Name'
    )
    ClienteLastNames = serializers.CharField(
        source='ClienteID.LastNames'
    )
    ClienteRut = serializers.CharField(
        source='ClienteID.Rut'
    )
    VentaLogType = serializers.CharField(
        source='VentaLogTypeID.Name'
    )
    Folio = serializers.CharField(
        source='ProyectoID.Name'
    )
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )
    Date = serializers.SerializerMethodField('get_date')
    Comment = serializers.SerializerMethodField('get_comment')
    User = UserProfileSerializer(
        source='UserID',
        allow_null=True
    )

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ClienteID', 'VentaLogTypeID', 'ProyectoID')
        return queryset

    class Meta:
        model = VentaLog
        fields = ('VentaLogID', 'VentaID', 'ProyectoID', 'ClienteName', 'ClienteLastNames',
                  'ClienteRut', 'VentaLogType', 'Date', 'Comment', 'Folio', 'User')

    def get_date(self, obj):
        try:
            return obj.Date.strftime("%Y-%m-%d")
        except AttributeError:
            return ""

    def get_comment(self, obj):
        if obj.Comment:
            return obj.Comment
        return ""


class VentaLogSerializer(serializers.ModelSerializer):

    ClienteName = serializers.CharField(
        source='ClienteID.Name'
    )
    ClienteLastNames = serializers.CharField(
        source='ClienteID.LastNames'
    )
    ClienteRut = serializers.CharField(
        source='ClienteID.Rut'
    )
    VendedorName = serializers.CharField(
        source='UserID.Name'
    )
    VendedorLastNames = serializers.CharField(
        source='UserID.LastNames'
    )
    VendedorRut = serializers.CharField(
        source='UserID.Rut'
    )
    VentaLogType = serializers.CharField(
        source='VentaLogTypeID.Name'
    )
    Date = serializers.SerializerMethodField('get_date')
    Comment = serializers.SerializerMethodField('get_comment')
    User = UserProfileSerializer(
        source='UserID',
        allow_null=True
    )
    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ClienteID', 'VentaLogTypeID')
        return queryset

    class Meta:
        model = VentaLog
        fields = ('VentaLogID', 'ClienteName', 'ClienteLastNames',
                  'ClienteRut', 'VendedorName', 'VendedorLastNames',
                  'VendedorRut', 'VentaLogType', 'Date', 'Comment',
                  'User')

    def get_date(self, obj):
        try:
            return obj.Date.strftime("%Y-%m-%d %H:%M:%S")
        except AttributeError:
            return ""

    def get_comment(self, obj):
        if obj.Comment:
            return obj.Comment
        return ""
class VentaLogUserSerializer(serializers.ModelSerializer):
    VentaLogType = serializers.CharField(
        source='VentaLogTypeID.Name'
    )
    Folio = serializers.CharField(
        source='ProyectoID.Name'
    )
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )
    User = UserProfileSerializer(
        source='UserID',
        allow_null=True
    )

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
           'VentaLogTypeID', 'ProyectoID')
        return queryset

    class Meta:
        model = VentaLog
        fields = ('VentaLogID', 'VentaID', 'ProyectoID', 'User',
                  'VentaLogType', 'Date', 'Comment', 'Folio')

    def get_comment(self, obj):
        if obj.Comment:
            return obj.Comment
        return ""

