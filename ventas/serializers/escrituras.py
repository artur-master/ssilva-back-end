from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework import serializers, status

from common import constants
from common.services import get_full_path_x, return_current_user, get_or_none
from ventas.models.escrituras import Escritura, AprobacionCredito
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
            ProyectoID=proyecto,
            EscrituraState=0
        )
    
    instance.save()

    # AprobacionCreditos.objects.filter(PromesaID=instance).delete()
    # AprobacionCreditos.objects.bulk_create()


class CreateAprobacionCreditoSerializer(serializers.ModelSerializer):
    EscrituraID = serializers.UUIDField(
        write_only=True
    )
    ClientApprovementLetter = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    ClientPersonalHealthStatement = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    AcFinancialInstitution = serializers.FileField(
        allow_empty_file=True,
        required=False
    )

    class Meta:
        model = AprobacionCredito
        fields = (
            'EscrituraID',
            'FormalCredit',
            'BankName',
            'ExecutiveName',
            'ExecutiveEmail',
            'ClientApprovementLetter',
            'ClientPersonalHealthStatement',
            'AcFinancialInstitution',
            'AcObservations',
            'AprobacionCreditoState',
            'DeclarePhysicalFolderState'
        )


class ListAprobacionCreditoSerializer(serializers.ModelSerializer):
    ClientPersonalHealthStatement = serializers.SerializerMethodField(
        'get_healthstatement_url')
    ClientApprovementLetter = serializers.SerializerMethodField(
        'get_approvement_url')
    AcFinancialInstitution = serializers.SerializerMethodField(
        'get_finicial_url')

    class Meta:
        model = AprobacionCredito
        fields = (
            'AprobacionCreditoID',
            'FormalCredit',
            'BankName',
            'ExecutiveName',
            'ExecutiveEmail',
            'ClientApprovementLetter',
            'ClientPersonalHealthStatement',
            'AcFinancialInstitution',
            'AcObservations',
            'AprobacionCreditoState'
        )

    def get_healthstatement_url(self, obj):
        if obj.ClientPersonalHealthStatement and hasattr(
                obj.ClientPersonalHealthStatement, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.ClientPersonalHealthStatement.url)
        else:
            return ""
    def get_approvement_url(self, obj):
        if obj.ClientApprovementLetter and hasattr(
                obj.ClientApprovementLetter, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.ClientApprovementLetter.url)
        else:
            return ""
    def get_finicial_url(self, obj):
        if obj.AcFinancialInstitution and hasattr(
                obj.AcFinancialInstitution, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.AcFinancialInstitution.url)
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
        fields = ('EscrituraID','ProyectoID', 'Proyecto', 'ClienteID',
                  'Cliente', 'Folio',
                  'EscrituraState', 'Inmuebles')

    def get_inmuebles(self, obj):
        inmuebles_promesa = PromesaInmueble.objects.filter(
            PromesaID=obj.PromesaID)
        serializer = ListReservaInmuebleSerializer(
            instance=inmuebles_promesa, context={'url': self.context['request']}, many=True)
        return serializer.data


class RetrieveEscrituraSerializer(serializers.ModelSerializer):    
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
    TasacionStateBank = serializers.SerializerMethodField('get_tasacion_statebank_url')
    TasacionSantander = serializers.SerializerMethodField('get_tasacion_santander_url')
    TasacionChileBank = serializers.SerializerMethodField('get_tasacion_chilebank_url')
    RevisionStateBank = serializers.SerializerMethodField('get_revision_statebank_url')
    RevisionSantander = serializers.SerializerMethodField('get_revision_santander_url')
    RevisionChileBank = serializers.SerializerMethodField('get_revision_chilebank_url')
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
    AprobacionCreditos = serializers.SerializerMethodField('get_aprobacion_creditos')

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
            'TasacionStateBank',
            'TasacionSantander',
            'TasacionChileBank',
            'RevisionStateBank',
            'RevisionConfirmoStateBank',
            'RevisionSantander',
            'RevisionConfirmoSantander',
            'RevisionChileBank',
            'RevisionConfirmoChileBank',
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
            'GPLoginRegistrationFile',
            'AprobacionCreditos'
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
    def get_tasacion_statebank_url(self, obj):
        if obj.TasacionStateBank and hasattr(
                obj.TasacionStateBank, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.TasacionStateBank.url)
        else:
            return ""
    def get_tasacion_santander_url(self, obj):
        if obj.TasacionSantander and hasattr(
                obj.TasacionSantander, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.TasacionSantander.url)
        else:
            return ""
    def get_tasacion_chilebank_url(self, obj):
        if obj.TasacionChileBank and hasattr(
                obj.TasacionChileBank, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.TasacionChileBank.url)
        else:
            return ""
    def get_revision_statebank_url(self, obj):
        if obj.RevisionStateBank and hasattr(
                obj.RevisionStateBank, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.RevisionStateBank.url)
        else:
            return ""
    def get_revision_santander_url(self, obj):
        if obj.RevisionSantander and hasattr(
                obj.RevisionSantander, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.RevisionSantander.url)
        else:
            return ""
    def get_revision_chilebank_url(self, obj):
        if obj.RevisionChileBank and hasattr(
                obj.RevisionChileBank, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.RevisionChileBank.url)
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
    def get_aprobacion_creditos(self, obj):
        aprobacionCreditos = AprobacionCredito.objects.filter(EscrituraID = obj)
        try:
            if aprobacionCreditos:
                serializer = ListAprobacionCreditoSerializer(
                        instance=aprobacionCreditos, many=True,
                        context={'request': self.context['request']}
                    )
                return serializer.data
            return [{'FormalCredit': '1', 'BankName': 'Banco Estado'}]
        except AttributeError:
            return [{'FormalCredit': '1', 'BankName': 'Banco Estado'}]


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
            'TasacionStateBank',
            'TasacionSantander',
            'TasacionChileBank',
            'RevisionStateBank',
            'RevisionConfirmoStateBank',
            'RevisionSantander',
            'RevisionConfirmoSantander',
            'RevisionChileBank',
            'RevisionConfirmoChileBank',
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
            'GPLoginRegistrationFile',
            'DeclarePhysicalFolderState'
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
        if 'TasacionStateBank' in validated_data:
            instance.TasacionStateBank = validated_data['TasacionStateBank']
        if 'TasacionSantander' in validated_data:
            instance.TasacionSantander = validated_data['TasacionSantander']
        if 'TasacionChileBank' in validated_data:
            instance.TasacionChileBank = validated_data['TasacionChileBank']
        if 'RevisionStateBank' in validated_data:
            instance.RevisionStateBank = validated_data['RevisionStateBank']
        if 'RevisionConfirmoStateBank' in validated_data:
            instance.RevisionConfirmoStateBank = validated_data['RevisionConfirmoStateBank']
        if 'RevisionSantander' in validated_data:
            instance.RevisionSantander = validated_data['RevisionSantander']
        if 'RevisionConfirmoSantander' in validated_data:
            instance.RevisionConfirmoSantander = validated_data['RevisionConfirmoSantander']
        if 'RevisionChileBank' in validated_data:
            instance.RevisionChileBank = validated_data['RevisionChileBank']
        if 'RevisionConfirmoChileBank' in validated_data:
            instance.RevisionConfirmoChileBank = validated_data['RevisionConfirmoChileBank']
        if 'MatrixDeed' in validated_data:
            instance.MatrixDeed = validated_data['MatrixDeed']
        if 'MatrixInstructions' in validated_data:
            instance.MatrixInstructions = validated_data['MatrixInstructions']
        if 'PromesaDeed' in validated_data:
            instance.PromesaDeed = validated_data['PromesaDeed']
        if 'PromesaCoinciden' in validated_data:
            instance.PromesaCoinciden = validated_data['PromesaCoinciden']
        if 'NoticeToClientDate' in validated_data:
            instance.NoticeToClientDate = validated_data['NoticeToClientDate']
        if 'BalanceFeeUF' in validated_data:
            instance.BalanceFeeUF = validated_data['BalanceFeeUF']
        if 'BalanceFund' in validated_data:
            instance.BalanceFund = validated_data['BalanceFund']
        if 'SignDate' in validated_data:
            instance.SignDate = validated_data['SignDate']
        if 'PaymentMethodBalance' in validated_data:
            instance.PaymentMethodBalance = validated_data['PaymentMethodBalance']
        if 'ChequeNumber' in validated_data:
            instance.ChequeNumber = validated_data['ChequeNumber']
        if 'Valor' in validated_data:
            instance.Valor = validated_data['Valor']
        if 'FetchaPago' in validated_data:
            instance.FetchaPago = validated_data['FetchaPago']
        if 'FetchaFirma' in validated_data:
            instance.FetchaFirma = validated_data['FetchaFirma']
        if 'InstructionObservacion' in validated_data:
            instance.InstructionObservacion = validated_data['InstructionObservacion']
        if 'RepertoireNumber' in validated_data:
            instance.RepertoireNumber = validated_data['RepertoireNumber']
        if 'StartDate' in validated_data:
            instance.StartDate = validated_data['StartDate']
        if 'RealEstateBilling' in validated_data:
            instance.RealEstateBilling = validated_data['RealEstateBilling']
        if 'InvoiceFile' in validated_data:
            instance.InvoiceFile = validated_data['InvoiceFile']
        if 'RealEstateSign' in validated_data:
            instance.RealEstateSign = validated_data['RealEstateSign']
        if 'RealEstateSignDate' in validated_data:
            instance.RealEstateSignDate = validated_data['RealEstateSignDate']
        if 'SignNotary' in validated_data:
            instance.SignNotary = validated_data['SignNotary']
        if 'SignNotaryDate' in validated_data:
            instance.SignNotaryDate = validated_data['SignNotaryDate']
        if 'SignDeedCompensation' in validated_data:
            instance.SignDeedCompensation = validated_data['SignDeedCompensation']
        if 'SignDeedCompensationDate' in validated_data:
            instance.SignDeedCompensationDate = validated_data['SignDeedCompensationDate']
        if 'SignSettelment' in validated_data:
            instance.pjw = validated_data['SignSettelment']
        if 'SignSettelmentDate' in validated_data:
            instance.SignSettelmentDate = validated_data['SignSettelmentDate']
        if 'SignPay' in validated_data:
            instance.SignPay = validated_data['SignPay']
        if 'SignPayDate' in validated_data:
            instance.SignPayDate = validated_data['SignPayDate']
        if 'MortgageLift' in validated_data:
            instance.MortgageLift = validated_data['MortgageLift']
        if 'MortgageLiftDate' in validated_data:
            instance.MortgageLiftDate = validated_data['MortgageLiftDate']
        if 'RealEstateConservator' in validated_data:
            instance.RealEstateConservator = validated_data['RealEstateConservator']
        if 'RealEstateConservatorFile' in validated_data:
            instance.RealEstateConservatorFile = validated_data['RealEstateConservatorFile']
        if 'SendCopiesToClient' in validated_data:
            instance.SendCopiesToClient = validated_data['SendCopiesToClient']
        if 'SendCopiesToClientDate' in validated_data:
            instance.SendCopiesToClientDate = validated_data['SendCopiesToClientDate']
        if 'SendCopiesToIN' in validated_data:
            instance.SendCopiesToIN = validated_data['SendCopiesToIN']
        if 'SendCopiesToINDate' in validated_data:
            instance.SendCopiesToINDate = validated_data['SendCopiesToINDate']
        if 'ProofDeed' in validated_data:
            instance.ProofDeed = validated_data['ProofDeed']
        if 'ProofDeedDate' in validated_data:
            instance.ProofDeedDate = validated_data['ProofDeedDate']
        if 'SubsidyState' in validated_data:
            instance.SubsidyState = validated_data['SubsidyState']
        if 'PaymentSubsidy' in validated_data:
            instance.PaymentSubsidy = validated_data['PaymentSubsidy']
        if 'PaymentSubsidyFile' in validated_data:
            instance.PaymentSubsidyFile = validated_data['PaymentSubsidyFile']
        if 'PaymentSavingIN' in validated_data:
            instance.PaymentSavingIN = validated_data['PaymentSavingIN']
        if 'PaymentSavingINFile' in validated_data:
            instance.PaymentSavingINFile = validated_data['PaymentSavingINFile']
        if 'INPaymentPending' in validated_data:
            instance.INPaymentPending = validated_data['INPaymentPending']
        if 'INPaymentPendingFile' in validated_data:
            instance.INPaymentPendingFile = validated_data['INPaymentPendingFile']
        if 'GuaranteeToClient' in validated_data:
            instance.GuaranteeToClient = validated_data['GuaranteeToClient']
        if 'GuaranteeToClientDate' in validated_data:
            instance.GuaranteeToClientDate = validated_data['GuaranteeToClientDate']
        if 'DeliveryProperty' in validated_data:
            instance.DeliveryProperty = validated_data['DeliveryProperty']
        if 'DeliveryPropertyDate' in validated_data:
            instance.DeliveryPropertyDate = validated_data['DeliveryPropertyDate']
        if 'GPLoginRegistration' in validated_data:
            instance.GPLoginRegistration = validated_data['GPLoginRegistration']
        if 'GPLoginRegistrationFile' in validated_data:
            instance.GPLoginRegistrationFile = validated_data['GPLoginRegistrationFile']         
        if 'DeclarePhysicalFolderState' in validated_data:
            instance.DeclarePhysicalFolderState = validated_data['DeclarePhysicalFolderState']         

        instance.save()

        return instance


class UpdateAprobacionCreditoSerializer(serializers.ModelSerializer):
    EscrituraState  = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True)
    AprobacionCreditos = CreateAprobacionCreditoSerializer(
        many=True,
        required=False
    )
    class Meta:
        model = Escritura
        fields = (
            'EscrituraID',
            'EscrituraState',
            'AprobacionCreditos'
        )
    
    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        proyecto = instance.ProyectoID
        
        instance.EscrituraState = validated_data['EscrituraState']
        
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
            escrituras = Escritura.objects.filter(ProyectoID=instance)
            for escritura in escrituras:
                escritura.EscrituraState=1.1
                escritura.save()        
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

