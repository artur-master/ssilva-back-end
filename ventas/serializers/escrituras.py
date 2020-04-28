from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework import serializers, status

from common import constants
from common.services import get_full_path_x, return_current_user, get_or_none
from ventas.models.escrituras import Escritura, AprobacionCreditos
from ventas.models.promesas import Promesa, PromesaInmueble
from empresas_and_proyectos.models.proyectos import UserProyectoType, UserProyecto, Proyecto
from ventas.models.ventas_logs import VentaLog, VentaLogType
from users.models import User, Permission
from ventas.serializers.clientes import ClienteSerializer
from ventas.serializers.reservas import ListReservaInmuebleSerializer

def create_escritura(proyecto, promesa):
    instance = Escritura.objects.filter(PromesaID=promesa)
    if len(instance) > 0:
        instance = instance[0]
    else:
        instance = Escritura(
            PromesaID=promesa,
            ProyectoID=proyecto
        )
    
    instance.save()

    # AprobacionCreditos.objects.filter(PromesaID=instance).delete()
    # AprobacionCreditos.objects.bulk_create()


class EscrituraSerializer(serializers.ModelSerializer):    
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID')
    Proyecto = serializers.CharField(
        source='ProyectoID.Name')
    EscrituraState = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True)
    Folio = serializers.CharField(
        source='PromesaID.Folio')    
    Cliente = ClienteSerializer(
        source='PromesaID.ClienteID',
        allow_null=True )
    CustomerCheckingAccount = serializers.SerializerMethodField('get_customer_url')
    PowersCharacteristics = serializers.SerializerMethodField('get_powers_url')       
    MatrixDeed = serializers.SerializerMethodField('get_matrix_deed_url')
    MatrixInstructions = serializers.SerializerMethodField('get_matrix_instructions_url')
    PromesaDeed = serializers.SerializerMethodField('get_promesa_url')    
    NoticeToClientDate = serializers.SerializerMethodField('get_notice_client_date')
    BalanceFeeUF = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True)
    BalanceFund = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True)
    SignDate = serializers.SerializerMethodField('get_sign_date')
    Valor = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True)
    FetchaPago = serializers.SerializerMethodField('get_pago_date')
    FetchaFirma = serializers.SerializerMethodField('get_firma_date')
    StartDate = serializers.SerializerMethodField('get_start_date')
    InvoiceFile = serializers.SerializerMethodField('get_invoice_url')
    RealEstateSignDate = serializers.SerializerMethodField('get_realestatesign_date')
    SignNotaryDate = serializers.SerializerMethodField('get_sign_notary_date')
    SignDeedCompensationDate = serializers.SerializerMethodField('get_signdeed_date')
    SignSettelmentDate = serializers.SerializerMethodField('get_signsettlement_date')
    SignPayDate = serializers.SerializerMethodField('get_signpay_date')
    MortgageLiftDate = serializers.SerializerMethodField('get_lift_date')
    RealEstateConservatorFile = serializers.SerializerMethodField('get_real_estate_url')
    SendCopiesToClientDate = serializers.SerializerMethodField('get_send_client_date')
    SendCopiesToINDate = serializers.SerializerMethodField('get_send_in_date')
    ProofDeedDate = serializers.SerializerMethodField('get_proof_deed_date')
    PaymentSubsidyFile  = serializers.SerializerMethodField('get_subsidy_url')
    PaymentSavingINFile = serializers.SerializerMethodField('get_saving_url')
    INPaymentPendingFile = serializers.SerializerMethodField('get_in_pending_url')
    GuaranteeToClientDate = serializers.SerializerMethodField('get_guarantee_client_date')
    DeliveryPropertyDate = serializers.SerializerMethodField('get_delivery_date')
    GPLoginRegistrationFile = serializers.SerializerMethodField('get_GP_url')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ProyectoID')
        # queryset = queryset.prefetch_related('EscrituraID')
        return queryset

    class Meta:
        model = Escritura
        fields = (
            'EscrituraID',
            'ProyectoID',
            'Proyecto',
            'Folio',
            'Cliente',
            'EscrituraState',
            'CarepetaFisicaState',
            'PromesaInstructions',
            'AgreedDeedDate',
            'DepartmentDeliveryDate',
            'SpecialWithdrawalClause',     
            'ModificationFinesClause',     
            'SpecialCommunication',
            'HasPromotion',
            'CustomerCheckingAccount',
            'PowersCharacteristics',
            # 'AprobacionCreditoState',
            # 'DeclarePhysicalFolderState',                
            'MatrixDeed',
            'MatrixInstructions',
            'PromesaDeed',
            'PromesaCoinciden',
            'NoticeToClientDate',
            'BalanceFeeUF',
            'BalanceFund',
            'SignDate',
            'PaymentMethodBalance',
            'ChequeNumber',
            'Valor',
            'FetchaPago',
            'FetchaFirma',
            'InstructionObservacion',
            'RepertoireNumber',
            'StartDate',
            'RealEstateBilling',
            'InvoiceFile',
            'RealEstateSign',
            'RealEstateSignDate',
            'SignNotary',
            'SignNotaryDate',
            'SignDeedCompensation',
            'SignDeedCompensationDate',
            'SignSettelment',
            'SignSettelmentDate',
            'SignPay',
            'SignPayDate',
            'MortgageLift',
            'MortgageLiftDate',
            'RealEstateConservator',
            'RealEstateConservatorFile',
            'SendCopiesToClient',
            'SendCopiesToClientDate',
            'SendCopiesToIN',
            'SendCopiesToINDate',
            'ProofDeed',
            'ProofDeedDate',
            'SubsidyState',
            'PaymentSubsidy',
            'PaymentSubsidyFile',
            'PaymentSavingIN',
            'PaymentSavingINFile',
            'INPaymentPending',
            'INPaymentPendingFile',
            'GuaranteeToClient',
            'GuaranteeToClientDate',
            'DeliveryProperty',
            'DeliveryPropertyDate',
            'GPLoginRegistration',
            'GPLoginRegistrationFile'
        )

    def get_customer_url(self, obj):
        if obj.CustomerCheckingAccount and hasattr(
                obj.CustomerCheckingAccount, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.CustomerCheckingAccount.url)
        else:
            return ""
    def get_powers_url(self, obj):
        if obj.PowersCharacteristics and hasattr(
                obj.PowersCharacteristics, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.PowersCharacteristics.url)
        else:
            return ""
    def get_matrix_deed_url(self, obj):
        if obj.MatrixDeed and hasattr(
                obj.MatrixDeed, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.MatrixDeed.url)
        else:
            return ""
    def get_matrix_instructions_url(self, obj):
        if obj.MatrixInstructions and hasattr(
                obj.MatrixInstructions, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.MatrixInstructions.url)
        else:
            return ""
    def get_promesa_url(self, obj):
        if obj.PromesaDeed and hasattr(
                obj.PromesaDeed, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.PromesaDeed.url)
        else:
            return ""
    def get_notice_client_date(self, obj):
        try:
            return obj.NoticeToClientDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_sign_date(self, obj):
        try:
            return obj.SignDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_pago_date(self, obj):
        try:
            return obj.FetchaPago.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_firma_date(self, obj):
        try:
            return obj.FetchaFirma.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_start_date(self, obj):
        try:
            return obj.StartDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_realestatesign_date(self, obj):
        try:
            return obj.RealEstateSignDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_sign_notary_date(self, obj):
        try:
            return obj.SignNotaryDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_signdeed_date(self, obj):
        try:
            return obj.SignDeedCompensationDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_signsettlement_date(self, obj):
        try:
            return obj.SignSettelmentDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_signpay_date(self, obj):
        try:
            return obj.SignPayDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_lift_date(self, obj):
        try:
            return obj.MortgageLiftDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_send_client_date(self, obj):
        try:
            return obj.SendCopiesToClientDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_send_in_date(self, obj):
        try:
            return obj.SendCopiesToINDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_proof_deed_date(self, obj):
        try:
            return obj.ProofDeedDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_guarantee_client_date(self, obj):
        try:
            return obj.GuaranteeToClientDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_delivery_date(self, obj):
        try:
            return obj.DeliveryPropertyDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_invoice_url(self, obj):
        if obj.InvoiceFile and hasattr(
                obj.InvoiceFile, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.InvoiceFile.url)
        else:
            return ""
    def get_real_estate_url(self, obj):
        if obj.RealEstateConservatorFile and hasattr(
                obj.RealEstateConservatorFile, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.RealEstateConservatorFile.url)
        else:
            return ""
    def get_subsidy_url(self, obj):
        if obj.PaymentSubsidyFile and hasattr(
                obj.PaymentSubsidyFile, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.PaymentSubsidyFile.url)
        else:
            return ""
    def get_saving_url(self, obj):
        if obj.PaymentSavingINFile and hasattr(
                obj.PaymentSavingINFile, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.PaymentSavingINFile.url)
        else:
            return ""
    def get_in_pending_url(self, obj):
        if obj.INPaymentPendingFile and hasattr(
                obj.INPaymentPendingFile, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.INPaymentPendingFile.url)
        else:
            return ""
    def get_GP_url(self, obj):
        if obj.GPLoginRegistrationFile and hasattr(
                obj.GPLoginRegistrationFile, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.GPLoginRegistrationFile.url)
        else:
            return ""
    

class ListEscrituraSerializer(serializers.ModelSerializer):
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )
    Proyecto = serializers.CharField(
        source='ProyectoID.Name'
    )
    Folio = serializers.CharField(
        source='PromesaID.Folio')    
    EscrituraState = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True)
    ClienteID = serializers.UUIDField(
        source='PromesaID.ClienteID.UserID' )
    Cliente = ClienteSerializer(
        source='PromesaID.ClienteID',
        allow_null=True )
    Inmuebles = serializers.SerializerMethodField('get_inmuebles')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ProyectoID', 'PromesaID')
        return queryset

    class Meta:
        model = Escritura
        fields = ('ProyectoID', 'Proyecto', 'ClienteID',
                  'Cliente', 'Folio',
                  'EscrituraState', 'Inmuebles')

    def get_inmuebles(self, obj):
        inmuebles_promesa = PromesaInmueble.objects.filter(
            PromesaID=obj.PromesaID)
        serializer = ListReservaInmuebleSerializer(
            instance=inmuebles_promesa, context={'url': self.context['request']}, many=True)
        return serializer.data


class UpdateEscrituraSerializer(serializers.ModelSerializer):
    EscrituraState  = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True)

    class Meta:
        model = Escritura
        fields = (
            'EscrituraID',
            'EscrituraState',
            'CarepetaFisicaState',
            'PromesaInstructions',
            'AgreedDeedDate',
            'DepartmentDeliveryDate',
            'SpecialWithdrawalClause',
            'ModificationFinesClause',
            'SpecialCommunication',
            'HasPromotion',
            'CustomerCheckingAccount',
            'PowersCharacteristics',
        )
    
    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        proyecto = instance.ProyectoID
        
        instance.EscrituraState = validated_data['EscrituraState']
        if 'CarepetaFisicaState' in validated_data:
            instance.CarepetaFisicaState = validated_data['CarepetaFisicaState']
        if 'PromesaInstructions' in validated_data:
            instance.PromesaInstructions = validated_data['PromesaInstructions']
        if 'AgreedDeedDate' in validated_data:
            instance.AgreedDeedDate = validated_data['AgreedDeedDate']
        if 'DepartmentDeliveryDate' in validated_data:
            instance.DepartmentDeliveryDate = validated_data['DepartmentDeliveryDate']
        if 'SpecialWithdrawalClause' in validated_data:
            instance.SpecialWithdrawalClause = validated_data['SpecialWithdrawalClause']
        if 'ModificationFinesClause' in validated_data:
            instance.ModificationFinesClause = validated_data['ModificationFinesClause']
        if 'SpecialCommunication' in validated_data:
            instance.SpecialCommunication = validated_data['SpecialCommunication']
        if 'HasPromotion' in validated_data:
            instance.HasPromotion = validated_data['HasPromotion']
        if 'CustomerCheckingAccount' in validated_data:
            instance.CustomerCheckingAccount = validated_data['CustomerCheckingAccount']
        if 'PowersCharacteristics' in validated_data:
            instance.PowersCharacteristics = validated_data['PowersCharacteristics']
        
        instance.save()

        return instance


class ConfirmProyectoSerializer(serializers.ModelSerializer):
    EscrituraProyectoState = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        required=False, allow_null=True
    )

    class Meta:
        model = Proyecto
        fields = (
            'ProyectoID',
            'EscrituraProyectoState'
        )

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        instance.EscrituraProyectoState = validated_data.get('EscrituraProyectoState')
        promesas = Promesa.objects.filter(
            ProyectoID=instance,
            PromesaState=constants.PROMESA_STATE[4])
        if promesas.exists():
            for promesa in promesas:
                create_escritura(instance, promesa)
            
        # Usuarios
        # jefe_proyecto = UserProyecto.objects.filter(
        #     ProyectoID=instance, UserProyectoTypeID=jefe_proyecto_type)

        # if jefe_proyecto.exists():
        #     eliminar_notificacion_proyecto_sin_jefe_proyecto(instance)
        # else:
        #     crear_notificacion_proyecto_sin_jefe_proyecto(
        #         instance, creator, usuarios_monitorea_proyectos)

        instance.save()
 
        return instance


class UpdateProyectoSerializer(serializers.ModelSerializer):
    EscrituraProyectoState = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        required=False, allow_null=True)
    SubmissionDate = serializers.DateField(
        write_only=True, required=False)
    ReceptionDate = serializers.DateField(
        write_only=True, required=False)
    RealEstateLawDate = serializers.DateField(
        write_only=True, required=False)
    RealEstateLawFile = serializers.FileField(
        allow_empty_file=True,
        required=False)
    PlansConservatorDate = serializers.DateField(
        write_only=True, required=False)
    PlansConservatorFile = serializers.FileField(
        allow_empty_file=True,
        required=False)
    DeedStartDate = serializers.DateField(
        write_only=True, required=False)
    DeliverDay = serializers.IntegerField(
        required=False, allow_null=True )
    StateBankReportDate = serializers.DateField(
        write_only=True, required=False)
    StateBankReportFile = serializers.FileField(
        allow_empty_file=True,
        required=False)
    StateBankObservations = serializers.JSONField(
        write_only=True, required=False )
    StateBankState = serializers.CharField(
        write_only=True, required=False)
    SantanderReportDate = serializers.DateField(
        write_only=True, required=False)
    SantanderReportFile = serializers.FileField(
        allow_empty_file=True,
        required=False)
    SantanderObservations = serializers.JSONField(
        write_only=True, required=False )
    SantanderState = serializers.CharField(
        write_only=True, required=False)
    ChileBankReportDate = serializers.DateField(
        write_only=True, required=False)
    ChileBankReportFile = serializers.FileField(
        allow_empty_file=True,
        required=False)
    ChileBankObservations = serializers.JSONField(
        write_only=True, required=False )
    ChileBankState = serializers.CharField(
        write_only=True, required=False )
    
    class Meta:
        model = Proyecto
        fields = (
            'ProyectoID',
            'EscrituraProyectoState',
            'SubmissionDate',
            'ReceptionDate',
            'RealEstateLawDate',
            'RealEstateLawFile',
            'PlansConservatorDate',
            'PlansConservatorFile',
            'DeedStartDate',
            'DeliverDay',
            'StateBankReportDate',
            'StateBankReportFile',
            'StateBankObservations',
            'StateBankState',
            'SantanderReportDate',
            'SantanderReportFile',
            'SantanderObservations',
            'SantanderState',
            'ChileBankReportDate',
            'ChileBankReportFile',
            'ChileBankObservations',
            'ChileBankState',
        )

    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        
        if 'EscrituraProyectoState' in validated_data:
            instance.EscrituraProyectoState = validated_data['EscrituraProyectoState']
        if 'SubmissionDate' in validated_data:
            instance.SubmissionDate = validated_data['SubmissionDate']
        if 'ReceptionDate' in validated_data:
            instance.ReceptionDate = validated_data['ReceptionDate']
        if 'RealEstateLawDate' in validated_data:
            instance.RealEstateLawDate = validated_data['RealEstateLawDate']
        if 'RealEstateLawFile' in validated_data:
            instance.RealEstateLawFile = validated_data['RealEstateLawFile']
        if 'PlansConservatorDate' in validated_data:
            instance.PlansConservatorDate = validated_data['PlansConservatorDate']
        if 'PlansConservatorFile' in validated_data:
            instance.PlansConservatorFile = validated_data['PlansConservatorFile']
        if 'DeedStartDate' in validated_data:
            instance.DeedStartDate = validated_data['DeedStartDate']
        if 'DeliverDay' in validated_data:
            instance.DeliverDay = validated_data['DeliverDay']
        if 'StateBankReportDate' in validated_data:
            instance.StateBankReportDate = validated_data['StateBankReportDate']
        if 'StateBankReportFile' in validated_data:
            instance.StateBankReportFile = validated_data['StateBankReportFile']
        if 'StateBankObservations' in validated_data:
            instance.StateBankObservations = validated_data['StateBankObservations']
        if 'StateBankState' in validated_data:
            instance.StateBankState = validated_data['StateBankState']
        if 'SantanderReportDate' in validated_data:
            instance.SantanderReportDate = validated_data['SantanderReportDate']
        if 'SantanderReportFile' in validated_data:
            instance.SantanderReportFile = validated_data['SantanderReportFile']
        if 'SantanderObservations' in validated_data:
            instance.SantanderObservations = validated_data['SantanderObservations']
        if 'SantanderState' in validated_data:
            instance.SantanderState = validated_data['SantanderState']
        if 'ChileBankReportDate' in validated_data:
            instance.ChileBankReportDate = validated_data['ChileBankReportDate']
        if 'ChileBankReportFile' in validated_data:
            instance.ChileBankReportFile = validated_data['ChileBankReportFile']
        if 'ChileBankObservations' in validated_data:
            instance.ChileBankObservations = validated_data['ChileBankObservations']
        if 'ChileBankState' in validated_data:
            instance.ChileBankState = validated_data['ChileBankState']
        
        instance.save()
 
        return instance

