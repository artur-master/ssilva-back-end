from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework import serializers, status

from common.services import get_full_path_x, return_current_user, get_or_none
from ventas.models.escrituras import (Escritura, TitleReports)
from empresas_and_proyectos.models.proyectos import Proyecto

class EscrituraSerializer(serializers.ModelSerializer):    
    ProyectoID = serializers.CharField(
        source='ProyectoID.ProyectoID'
    )
    Proyecto = serializers.CharField(
        source='ProyectoID.Name'
    )
    EscrituraState = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True)
    SubmissionDate = serializers.SerializerMethodField('get_submission_date')
    CustomerCheckingAccount = serializers.SerializerMethodField('get_customer_url')
    PowersCharacteristics = serializers.SerializerMethodField('get_powers_url')
    ReceptionDate = serializers.SerializerMethodField('get_reception_date')
    RealEstateLawDate = serializers.SerializerMethodField('get_realestatelaw_date')
    RealEstateLawFile = serializers.SerializerMethodField('get_realestate_url')
    PlansConservatorDate = serializers.SerializerMethodField('get_plansconservator_date')
    PlansConservatorFile = serializers.SerializerMethodField('get_plans_url')
    DeedStartDate = serializers.SerializerMethodField('get_deedstart_date')        
    MatrixDeed = serializers.SerializerMethodField('get_matrix_deed_url')
    MatrixInstructions = serializers.SerializerMethodField('get_matrix_instructions_url')
    PromesaDeed = serializers.SerializerMethodField('get_promesa_url')

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
            'EscrituraState',
            'SubmissionDate',
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
            'ReceptionDate',
            'RealEstateLawDate',
            'RealEstateLawFile',
            'PlansConservatorDate',
            'PlansConservatorFile',
            'DeedStartDate',
            'AprobacionCreditoState',
            'DeclarePhysicalFolderState',                
            'MatrixDeed',
            'MatrixInstructions',
            'PromesaDeed',
            'PromesaCoinciden',
        )

    def get_submission_date(self, obj):
        try:
            return obj.SubmissionDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_reception_date(self, obj):
        try:
            return obj.ReceptionDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_realestatelaw_date(self, obj):
        try:
            return obj.RealEstateLawDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_plansconservator_date(self, obj):
        try:
            return obj.PlansConservatorDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_deedstart_date(self, obj):
        try:
            return obj.DeedStartDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""

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
    def get_realestate_url(self, obj):
        if obj.RealEstateLawFile and hasattr(
                obj.RealEstateLawFile, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.RealEstateLawFile.url)
        else:
            return ""
    def get_plans_url(self, obj):
        if obj.PlansConservatorFile and hasattr(
                obj.PlansConservatorFile, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.PlansConservatorFile.url)
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

class CreateEscrituraSerializer(serializers.ModelSerializer):
    ProyectoID = serializers.UUIDField(
        write_only=True)
    EscrituraState  = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True)

    class Meta:
        model = Escritura
        fields = ('ProyectoID', 'EscrituraState')
    
    def create(self, validated_data):
        current_user = return_current_user(self)

        proyecto = Proyecto.objects.get(
            ProyectoID=validated_data['ProyectoID'])
        
        instance = Escritura.objects.create(
            ProyectoID=proyecto,
            EscrituraState=validated_data['EscrituraState'])
        
        return instance

class UpdateEscrituraSerializer(serializers.ModelSerializer):
    EscrituraState  = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True)
    SubmissionDate = serializers.DateField(
        write_only=True,
        allow_null=True)    

    class Meta:
        model = Escritura
        fields = (
            'EscrituraID',
            'EscrituraState',
            'SubmissionDate',
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
        if 'SubmissionDate' in validated_data:
            instance.SubmissionDate = validated_data['SubmissionDate']
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