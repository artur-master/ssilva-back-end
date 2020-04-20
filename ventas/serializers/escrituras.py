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
        )

    def get_submission_date(self, obj):
        try:
            return obj.SubmissionDate.strftime("%Y-%m-%d")
        except AttributeError:
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
        )
    
    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        proyecto = instance.ProyectoID
        
        instance.EscrituraState = validated_data['EscrituraState']
        if 'SubmissionDate' in validated_data:
            instance.SubmissionDate = validated_data['SubmissionDate']
        
        instance.save()

        return instance