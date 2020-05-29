from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from common import constants
from common.generate_pdf import render_create_proyecto_to_pdf, render_update_proyecto_to_pdf
from common.models import Notification, Comuna, ContactInfoType, NotificationType, Provincia, Region
from common.notifications import (
    crear_notificacion_proyecto_sin_jefe_proyecto,
    crear_notificacion_proyecto_sin_representantes,
    crear_notificacion_proyecto_sin_vendedores,
    crear_notificacion_proyecto_sin_asistentes_comerciales,
    crear_notificacion_proyecto_sin_aprobador,
    crear_notificacion_proyecto_sin_institucion_financiera,
    crear_notificacion_proyecto_sin_aseguradora,
    crear_notificacion_proyecto_sin_constructora,
    crear_notificacion_proyecto_sin_inmuebles,
    crear_notificacion_rechazar_proyecto,
    crear_notificacion_usuarios_aprueba_inmuebles,
    crear_notificacion_proyecto_pendiente_aprobacion,
    crear_notificacion_usuarios_monitorea_proyectos,
    crear_notificacion_proyecto_sin_borrador_promesa,
    eliminar_notificacion_proyecto_sin_representante,
    eliminar_notificacion_proyecto_sin_jefe_proyecto,
    eliminar_notificacion_proyecto_sin_vendedores,
    eliminar_notificacion_proyecto_sin_asistentes_comerciales,
    eliminar_notificacion_proyecto_sin_aprobador,
    eliminar_notificacion_proyecto_sin_institucion_financiera,
    eliminar_notificacion_proyecto_sin_aseguradora,
    eliminar_notificacion_proyecto_sin_constructora,
    eliminar_notificacion_proyecto_aprobacion,
    eliminar_notificacion_proyecto_pendiente_aprobacion,
    eliminar_notificacion_borrador_promesa,
    crear_notificacion_aprobar_proyecto)
from common.serializers.notifications import NotificationSerializer, NotificationRetrieveProyectoSerializer
from common.services import get_or_none, return_current_user, get_full_path_x, verify_data_proyecto
from common.snippets.graphs.proyectos import return_graph
from common.validations import CustomValidation
from empresas_and_proyectos.models.aseguradoras import Aseguradora
from empresas_and_proyectos.models.constructoras import Constructora
from empresas_and_proyectos.models.etapas import (
    Etapa,
    EtapaState)
from empresas_and_proyectos.models.inmobiliarias import Inmobiliaria
from empresas_and_proyectos.models.instituciones_financieras import (
    InstitucionFinanciera)
from empresas_and_proyectos.models.project_documents import ProjectDocument
from empresas_and_proyectos.models.proyectos import (
    UserProyectoType,
    UserProyecto,
    ProyectoAseguradora,
    ProyectoContactInfo,
    Proyecto,
    ProyectoApprovalState)
from empresas_and_proyectos.models.proyectos_logs import (
    ProyectoLog,
    ProyectoLogType)
from empresas_and_proyectos.models.states import (
    PlanMediosState,
    BorradorPromesaState,
    IngresoComisionesState)
from empresas_and_proyectos.serializers.etapas import EtapaStateSerializer
from history.models import (
    CounterHistory,
    HistoricalProyecto,
    HistoricalUserProyecto,
    HistoricalProyectoAseguradora,
    HistoricalProyectoContactInfo)
from sgi_web_back_project import settings
from users.models import User, Permission
from ventas.models.cotizaciones import Cotizacion
from ventas.models.counter_folios import CounterFolio
from ventas.models.ofertas import Oferta
from ventas.models.promesas import Promesa
from ventas.models.reservas import Reserva
from ventas.models.escrituras import Escritura


class UserProyectoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProyectoType
        fields = ('UserProyectoTypeID', 'Name')


class UserProyectoSerializer(serializers.ModelSerializer):
    Name = serializers.CharField(
        source='UserID.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    LastNames = serializers.CharField(
        source='UserID.LastNames',
        read_only=True,
        required=False,
        allow_null=True
    )
    Rut = serializers.CharField(
        source='UserID.Rut',
        read_only=True,
        required=False,
        allow_null=True
    )
    UserID = serializers.CharField(
        source='UserID.UserID',
        read_only=True,
        required=False,
        allow_null=True
    )
    Proyecto = serializers.CharField(
        source='ProyectoID.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    UserProyectoType = serializers.CharField(
        source='UserProyectoTypeID.Name',
        read_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = UserProyecto
        fields = ('Name', 'LastNames', 'Rut', 'UserID',
                  'Proyecto', 'UserProyectoType')


class ProyectoAseguradoraSerializer(serializers.ModelSerializer):
    ProyectoAseguradoraID = serializers.CharField(
        read_only=True,
        required=False,
        allow_null=True
    )
    AseguradoraID = serializers.CharField(
        source='AseguradoraID.AseguradoraID',
        read_only=True,
        required=False,
        allow_null=True
    )
    Aseguradora = serializers.CharField(
        source='AseguradoraID',
        read_only=True,
        required=False,
        allow_null=True
    )
    Amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True,
        required=False,
        allow_null=True
    )
    ExpirationDate = serializers.DateTimeField(
        read_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = ProyectoAseguradora
        fields = ('ProyectoAseguradoraID', 'AseguradoraID',
                  'Aseguradora', 'Amount', 'ExpirationDate')


class ProyectoContactInfoSerializer(serializers.ModelSerializer):
    ContactInfoTypeID = serializers.CharField(
        source='ContactInfoTypeID.ContactInfoTypeID',
        read_only=True,
        required=False,
        allow_null=True
    )
    ContactInfoType = serializers.CharField(
        source='ContactInfoTypeID.Name',
        read_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = ProyectoContactInfo
        fields = (
            'ContactInfoTypeID',
            'ContactInfoType',
            'Value')


class ProyectoSerializer(serializers.ModelSerializer):
    Comuna = serializers.CharField(
        source='ComunaID.Name',
        read_only=True,
        required=False,
        allow_null=True
    )

    UsersProyecto = serializers.SerializerMethodField('get_usuarios_proyectos')
    Notifications = serializers.SerializerMethodField('get_notificaciones')
    ProyectoApprovalState = serializers.CharField(
        source='ProyectoApprovalState.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    PlanMediosState = serializers.CharField(
        source='PlanMediosState.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    BorradorPromesaState = serializers.CharField(
        source='BorradorPromesaState.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    IngresoComisionesState = serializers.CharField(
        source='IngresoComisionesState.Name',
        read_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Proyecto
        fields = ('ProyectoID', 'Name', 'Symbol', 'Address', 'Comuna', 'Arquitecto',
                  'Notifications',
                  'UsersProyecto',
                  'ProyectoApprovalState',
                  'PlanMediosState',
                  'BorradorPromesaState',
                  'IngresoComisionesState',)

    def get_notificaciones(self, obj):
        notifications = Notification.objects.filter(
            TableID=obj.ProyectoID)
        serializer = NotificationSerializer(instance=notifications, many=True)
        return serializer.data

    def get_usuarios_proyectos(self, obj):
        usuarios_proyectos = UserProyecto.objects.filter(ProyectoID=obj)
        serializer = UserProyectoSerializer(
            instance=usuarios_proyectos, many=True)
        return serializer.data


class ProyectoLogTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProyectoLogType
        fields = ('ProyectoLogTypeID', 'Name', 'MaximunDays')


class ProyectoLogPDFSerializer(serializers.ModelSerializer):
    ProyectoLogID = serializers.CharField(
        read_only=True,
        required=False,
        allow_null=True
    )
    UserName = serializers.CharField(
        source='UserID.Name',
        required=False,
        allow_null=True
    )
    UserLastNames = serializers.CharField(
        source='UserID.LastNames',
        required=False,
        allow_null=True
    )
    UserRut = serializers.CharField(
        source='UserID.Rut',
        required=False,
        allow_null=True
    )
    ProyectoLogType = serializers.CharField(
        source='ProyectoLogTypeID.Name',
        required=False,
        allow_null=True
    )
    ProyectoDetailDocument = serializers.SerializerMethodField(
        'get_proyecto_detail_url')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'UserID', 'ProyectoID', 'ProyectoLogTypeID')
        return queryset

    class Meta:
        model = ProyectoLog
        fields = ('ProyectoLogID', 'ProyectoLogType', 'UserName',
                  'UserLastNames', 'UserRut', 'Date',
                  'Comment', 'ProyectoDetailDocument',)

    def get_proyecto_detail_url(self, obj):
        if obj.ProyectoDetailDocument and hasattr(
                obj.ProyectoDetailDocument, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.ProyectoDetailDocument.url)
        else:
            return ""


class ProjectDocumentSerializer(serializers.ModelSerializer):
    # marketing
    marketing_excel = serializers.SerializerMethodField()
    marketing_pdf = serializers.SerializerMethodField()
    # legal
    counter_word = serializers.SerializerMethodField()
    counter_pdf = serializers.SerializerMethodField()
    credit_word = serializers.SerializerMethodField()
    credit_pdf = serializers.SerializerMethodField()
    company_word = serializers.SerializerMethodField()
    company_pdf = serializers.SerializerMethodField()
    brokerage_contract = serializers.SerializerMethodField()
    domain_certificate = serializers.SerializerMethodField()
    company_deed = serializers.SerializerMethodField()
    approved_price_list = serializers.SerializerMethodField()
    title_folder = serializers.SerializerMethodField()

    class Meta:
        model = ProjectDocument
        fields = (
            'marketing_excel',
            'marketing_pdf',
            'counter_word',
            'counter_pdf',
            'credit_word',
            'credit_pdf',
            'company_word',
            'company_pdf',
            'brokerage_contract',
            'domain_certificate',
            'company_deed',
            'approved_price_list',
            'title_folder'
        )

    @property
    def base_url(self):
        return "http://" + get_current_site(self.context.get('request')).domain

    def get_attachment_url(self, obj, doc_type):
        try:
            project_id = self.context['request'].parser_context['kwargs']['ProyectoID']
            document = obj.get(DocumentType=doc_type, ProjectID=project_id)
            url = self.base_url + document.Document.url
            return {
                "url": url,
                "state": document.State,
                "document_type": doc_type,
                "no_existed": document.NoExisted
            }
        except ValueError:
            return {
                "url": None,
                "state": document.State,
                "document_type": doc_type,
                "no_existed": constants.FILE_NON_EXISTED
            }
        except Exception as ex:
            return None

    def get_marketing_excel(self, obj):
        return self.get_attachment_url(obj, constants.MarketingDocumentTypes.MARKETING_EXCEL)

    def get_marketing_pdf(self, obj):
        return self.get_attachment_url(obj, constants.MarketingDocumentTypes.MARKETING_PDF)

    def get_counter_word(self, obj):
        return self.get_attachment_url(obj, constants.LegalDocumentTypes.COUNTER_WORD)

    def get_counter_pdf(self, obj):
        return self.get_attachment_url(obj, constants.LegalDocumentTypes.COUNTER_PDF)

    def get_credit_word(self, obj):
        return self.get_attachment_url(obj, constants.LegalDocumentTypes.CREDIT_WORD)

    def get_credit_pdf(self, obj):
        return self.get_attachment_url(obj, constants.LegalDocumentTypes.CREDIT_PDF)

    def get_company_word(self, obj):
        return self.get_attachment_url(obj, constants.LegalDocumentTypes.COMPANY_WORD)

    def get_company_pdf(self, obj):
        return self.get_attachment_url(obj, constants.LegalDocumentTypes.COMPANY_PDF)

    def get_brokerage_contract(self, obj):
        return self.get_attachment_url(obj, constants.LegalDocumentTypes.BROKERAGE_CONTRACT)

    def get_domain_certificate(self, obj):
        return self.get_attachment_url(obj, constants.LegalDocumentTypes.DOMAIN_CERTIFICATE)

    def get_company_deed(self, obj):
        return self.get_attachment_url(obj, constants.LegalDocumentTypes.COMPANY_DEED)

    def get_approved_price_list(self, obj):
        return self.get_attachment_url(obj, constants.LegalDocumentTypes.APPROVED_PRICE_LIST)

    def get_title_folder(self, obj):
        return self.get_attachment_url(obj, constants.LegalDocumentTypes.TITLE_FOLDER)


class EtapaProyectoSerializer(serializers.ModelSerializer):
    EtapaStateID = serializers.CharField(source='EtapaStateID.Name')

    class Meta:
        model = Etapa
        exclude = ('ProyectoID', 'id')


class RetrieveProyectoSerializer(serializers.ModelSerializer):
    InstitucionFinancieraID = serializers.CharField(
        source='InstitucionFinancieraID.InstitucionFinancieraID',
        read_only=True,
        required=False,
        allow_null=True
    )
    InstitucionFinanciera = serializers.CharField(
        source='InstitucionFinancieraID.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    InmobiliariaID = serializers.CharField(
        source='InmobiliariaID.InmobiliariaID',
        read_only=True,
        required=False,
        allow_null=True
    )
    Inmobiliaria = serializers.CharField(
        source='InmobiliariaID.RazonSocial',
        read_only=True,
        required=False,
        allow_null=True
    )
    ConstructoraID = serializers.CharField(
        source='ConstructoraID.ConstructoraID',
        read_only=True,
        required=False,
        allow_null=True
    )
    Constructora = serializers.CharField(
        source='ConstructoraID.RazonSocial',
        read_only=True,
        required=False,
        allow_null=True
    )
    Comuna = serializers.CharField(
        source='ComunaID.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    ComunaID = serializers.CharField(
        source='ComunaID.ComunaID',
        read_only=True,
        required=False,
        allow_null=True
    )
    Provincia = serializers.CharField(
        source='ComunaID.ProvinciaID.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    Region = serializers.CharField(
        source='ComunaID.ProvinciaID.RegionID.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    ProyectoApprovalState = serializers.CharField(
        source='ProyectoApprovalState.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    PlanMediosState = serializers.CharField(
        source='PlanMediosState.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    BorradorPromesaState = serializers.CharField(
        source='BorradorPromesaState.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    IngresoComisionesState = serializers.CharField(
        source='IngresoComisionesState.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    EtapaState = EtapaStateSerializer(
        source='EtapaStateID',
        read_only=True,
        required=False,
        allow_null=True
    )
    ContactInfo = serializers.SerializerMethodField('get_proyectos_contact_info')
    Aseguradora = serializers.SerializerMethodField('get_proyecto_aseguradora')
    UsersProyecto = serializers.SerializerMethodField('get_usuarios_proyectos')
    Notifications = serializers.SerializerMethodField('get_notificaciones')
    IsFinished = serializers.SerializerMethodField('get_state_proyecto')
    Graph = serializers.SerializerMethodField('get_graph')
    Documentos = ProjectDocumentSerializer(
        source='Documents',
        read_only=True
    )
    EntregaInmediata = serializers.BooleanField()
    Etapa = EtapaProyectoSerializer(
        source='proyecto_etapa',
        many=True
    )

    Metadata = serializers.SerializerMethodField('get_project_meta')

    #Escritura
    EscrituraProyectoState = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False, read_only=True)
    SubmissionDate = serializers.SerializerMethodField('get_submission_date')
    ReceptionDate = serializers.SerializerMethodField('get_reception_date')
    RealEstateLawDate = serializers.SerializerMethodField('get_realestatelaw_date')
    RealEstateLawFile = serializers.SerializerMethodField('get_realestate_url')
    PlansConservatorDate = serializers.SerializerMethodField('get_plansconservator_date')
    PlansConservatorFile = serializers.SerializerMethodField('get_plans_url')
    DeedStartDate = serializers.SerializerMethodField('get_deedstart_date')
    StateBankReportFile = serializers.SerializerMethodField('get_statebank_url')
    StateBankObservations = serializers.JSONField( read_only=True, required=False )
    SantanderReportFile = serializers.SerializerMethodField('get_santander_url')
    SantanderObservations = serializers.JSONField( read_only=True,required=False )
    ChileBankReportFile = serializers.SerializerMethodField('get_chilebank_url')
    ChileBankObservations = serializers.JSONField(read_only=True,required=False)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related(
            'ProyectoAseguradoraID',
            'InmobiliariaID',
            'ConstructoraID')
        queryset = queryset.prefetch_related('ContactInfo', 'UserProyecto')
        return queryset

    class Meta:
        model = Proyecto
        fields = (
            'ProyectoID',
            'Name',
            'Arquitecto',
            'Symbol',
            'Address',
            'ContactInfo',
            'InstitucionFinancieraID',
            'MoreThanOneEtapa',
            'InstitucionFinanciera',
            'InmobiliariaID',
            'Inmobiliaria',
            'ConstructoraID',
            'Constructora',
            'Provincia',
            'Comuna',
            'Region',
            'ProyectoApprovalState',
            'PlanMediosState',
            'BorradorPromesaState',
            'IngresoComisionesState',
            'CotizacionDuration',
            'GuaranteeAmount',
            'ContadoMontoPromesa',
            'ContadoMontoCuotas',
            'ContadoMontoEscrituraContado',
            'ContadoAhorroPlus',
            'ContadoAhorroPlusMaxDiscounts',
            'CreditoMontoPromesa',
            'CreditoMontoCuotas',
            'CreditoMontoEscrituraContado',
            'CreditoAhorroPlus',
            'CreditoAhorroPlusMaxDiscounts',
            'DiscountMaxPercent',
            'Aseguradora',
            'UsersProyecto',
            'Notifications',
            'IsFinished',
            'Graph',
            'EtapaState',
            'EntregaInmediata',
            'Documentos',
            'ComunaID',
            'Etapa',
            'Metadata',
            'MaxCuotas',
            'MetasUf',
            'MetasPromesas',
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

    def get_notificaciones(self, obj):
        notificacions = Notification.objects.filter(
            TableID=obj.ProyectoID, UserID__Rut=self.context['request'].user)
        serializer = NotificationRetrieveProyectoSerializer(instance=notificacions, many=True)
        return serializer.data

    def get_proyectos_contact_info(self, obj):
        proyectos_contact_info = ProyectoContactInfo.objects.filter(
            ProyectoID=obj)
        serializer = ProyectoContactInfoSerializer(
            instance=proyectos_contact_info, many=True)
        return serializer.data

    def get_proyecto_aseguradora(self, obj):
        proyecto_aseguradora = get_or_none(
            ProyectoAseguradora, aseguradora_proyecto=obj)
        serializer = ProyectoAseguradoraSerializer(
            instance=proyecto_aseguradora)
        return serializer.data

    def get_usuarios_proyectos(self, obj):
        usuarios_proyectos = UserProyecto.objects.filter(ProyectoID=obj)
        serializer = UserProyectoSerializer(
            instance=usuarios_proyectos, many=True)
        return serializer.data

    def get_graph(self, obj):
        graph = return_graph(obj)
        if obj.ProyectoApprovalState.Name == constants.PROYECTO_APPROVAL_STATE[3]:
            return {}
        else:
            return graph

    def get_state_proyecto(self, obj):
        if obj.ProyectoApprovalState.Name == constants.PROYECTO_APPROVAL_STATE[3]:
            return True
        else:
            return False

    def get_project_meta(self, obj):
        quotation_count = Cotizacion.objects.filter(ProyectoID=obj).count()
        reservation_count = Reserva.objects.filter(ProyectoID=obj).count()
        promesa_count = Promesa.objects.filter(ProyectoID=obj).count()
        offer_count = Oferta.objects.filter(ProyectoID=obj).count()
        escritura_count = Escritura.objects.filter(ProyectoID=obj).count()
        counter = dict(Quotation=quotation_count,
                       Reservation=reservation_count,
                       Promesa=promesa_count,
                       Offer=offer_count,
                       Escritura=escritura_count)
        result = dict(Count=counter)
        return result

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
    def get_realestate_url(self, obj):
        if obj.RealEstateLawFile and hasattr(
                obj.RealEstateLawFile, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.RealEstateLawFile.url)
        else:
            return ""
    def get_plansconservator_date(self, obj):
        try:
            return obj.PlansConservatorDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_plans_url(self, obj):
        if obj.PlansConservatorFile and hasattr(
                obj.PlansConservatorFile, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.PlansConservatorFile.url)
        else:
            return ""
    def get_deedstart_date(self, obj):
        try:
            return obj.DeedStartDate.strftime("%Y-%m-%d")
        except AttributeError:
            return ""
    def get_statebank_url(self, obj):
        if obj.StateBankReportFile and hasattr(
                obj.StateBankReportFile, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.StateBankReportFile.url)
        else:
            return ""
    def get_santander_url(self, obj):
        if obj.SantanderReportFile and hasattr(
                obj.SantanderReportFile, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.SantanderReportFile.url)
        else:
            return ""
    def get_chilebank_url(self, obj):
        if obj.ChileBankReportFile and hasattr(
                obj.ChileBankReportFile, 'url'):
            absolute_url = get_full_path_x(self.context['request'])
            return "%s%s" % (absolute_url, obj.ChileBankReportFile.url)
        else:
            return ""


class ApproveCreateProyectoLegalSerializer(serializers.ModelSerializer):
    ProyectoApprovalState = serializers.CharField(
        source='ProyectoApprovalState.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    Comment = serializers.CharField(
        write_only=True,
        allow_blank=True,
        required=False,
        allow_null=True
    )
    Name = serializers.CharField(
        read_only=True,
        required=False,
        allow_null=True
    )
    Resolution = serializers.BooleanField(
        write_only=True,
        required=False
    )

    class Meta:
        model = Proyecto
        fields = ('ProyectoID', 'Name', 'ProyectoApprovalState',
                  'Resolution', 'Comment')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        comment = validated_data.pop('Comment')
        resolution = validated_data.pop('Resolution')

        # Permiso Monitorea Proyectos
        permission = Permission.objects.get(Name=constants.PERMISSIONS[14])

        # Tipos de Usuarios
        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])

        # Usuarios
        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance, UserProyectoTypeID=jefe_proyecto_type)

        if resolution:
            if instance.ProyectoApprovalState.Name == constants.PROYECTO_APPROVAL_STATE[3]:
                raise CustomValidation(
                    "Proyecto ya está aprobado",
                    status_code=status.HTTP_409_CONFLICT)

            if instance.ProyectoApprovalState.Name == constants.PROYECTO_APPROVAL_STATE[2]:
                raise CustomValidation(
                    "Proyecto ya fue aprobado por legal",
                    status_code=status.HTTP_409_CONFLICT)

            proyecto_approval_state = ProyectoApprovalState.objects.get(Name=constants.PROYECTO_APPROVAL_STATE[2])
            proyecto_log_type = ProyectoLogType.objects.get(
                Name=constants.PROYECTO_LOG_TYPE[1])

            ProyectoLog.objects.create(
                UserID=current_user,
                ProyectoID=instance,
                ProyectoLogTypeID=proyecto_log_type,
                Comment=comment
            )

            eliminar_notificacion_proyecto_aprobacion(instance)
            eliminar_notificacion_proyecto_pendiente_aprobacion(instance)

            # Crear notificacion a usuarios aprueba proyectos
            permission = Permission.objects.get(Name=constants.PERMISSIONS[14])

            usuarios_monitorea_proyectos = User.objects.filter(
                RoleID__PermissionID=permission
            )

            if crear_notificacion_usuarios_monitorea_proyectos(instance, usuarios_monitorea_proyectos):
                raise CustomValidation(
                    "Proyecto ya está en espera de aprobación",
                    status_code=status.HTTP_409_CONFLICT)
            else:
                area_approve = constants.AREA_APPROVE[1]
                crear_notificacion_proyecto_pendiente_aprobacion(
                    instance, jefe_proyecto, area_approve)

                area_approve = constants.AREA_APPROVE[0]
                crear_notificacion_aprobar_proyecto(instance, jefe_proyecto, area_approve)
        else:
            if instance.ProyectoApprovalState.Name == constants.PROYECTO_APPROVAL_STATE[2]:
                raise CustomValidation(
                    "Proyecto ya ha sido aprobado por legal, no se puede rechazar",
                    status_code=status.HTTP_409_CONFLICT)

            proyecto_approval_state = ProyectoApprovalState.objects.get(
                Name=constants.PROYECTO_APPROVAL_STATE[1])
            proyecto_log_type = ProyectoLogType.objects.get(
                Name=constants.PROYECTO_LOG_TYPE[5])

            ProyectoLog.objects.create(
                UserID=current_user,
                ProyectoID=instance,
                ProyectoLogTypeID=proyecto_log_type,
                Comment=comment
            )

            crear_notificacion_rechazar_proyecto(instance, jefe_proyecto)
            eliminar_notificacion_proyecto_aprobacion(instance)
            eliminar_notificacion_proyecto_pendiente_aprobacion(instance)

        instance.ProyectoApprovalState = proyecto_approval_state
        instance.save()

        return instance


class ApproveCreateProyectoGerenciaSerializer(serializers.ModelSerializer):
    ProyectoApprovalState = serializers.CharField(
        source='ProyectoApprovalState.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    Comment = serializers.CharField(
        write_only=True,
        allow_blank=True,
        required=False,
        allow_null=True
    )
    Name = serializers.CharField(
        read_only=True,
        required=False,
        allow_null=True
    )
    Resolution = serializers.BooleanField(
        write_only=True,
        required=False
    )

    class Meta:
        model = Proyecto
        fields = ('ProyectoID', 'Name', 'ProyectoApprovalState',
                  'Resolution', 'Comment')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        comment = validated_data.pop('Comment')
        resolution = validated_data.pop('Resolution')

        # Permiso Monitorea Proyectos
        permission = Permission.objects.get(Name=constants.PERMISSIONS[14])

        # Tipos de Usuarios
        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])

        # Usuarios
        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance, UserProyectoTypeID=jefe_proyecto_type)

        # Area Gerencia
        area_approve = constants.AREA_APPROVE[1]

        if resolution:
            if instance.ProyectoApprovalState.Name == constants.PROYECTO_APPROVAL_STATE[3]:
                raise CustomValidation(
                    "Proyecto ya está aprobado",
                    status_code=status.HTTP_409_CONFLICT)

            proyecto_approval_state = ProyectoApprovalState.objects.get(
                Name=constants.PROYECTO_APPROVAL_STATE[3])
            proyecto_log_type = ProyectoLogType.objects.get(
                Name=constants.PROYECTO_LOG_TYPE[9])

            ProyectoLog.objects.create(
                UserID=current_user,
                ProyectoID=instance,
                ProyectoLogTypeID=proyecto_log_type,
                Comment=comment
            )

            eliminar_notificacion_proyecto_aprobacion(instance)
            eliminar_notificacion_proyecto_pendiente_aprobacion(instance)
            crear_notificacion_aprobar_proyecto(instance, jefe_proyecto, area_approve)
        else:
            if instance.ProyectoApprovalState.Name == constants.PROYECTO_APPROVAL_STATE[3]:
                raise CustomValidation(
                    "Proyecto ya esta aprobado, no se puede rechazar",
                    status_code=status.HTTP_409_CONFLICT)

            proyecto_approval_state = ProyectoApprovalState.objects.get(
                Name=constants.PROYECTO_APPROVAL_STATE[1])
            proyecto_log_type = ProyectoLogType.objects.get(
                Name=constants.PROYECTO_LOG_TYPE[10])

            ProyectoLog.objects.create(
                UserID=current_user,
                ProyectoID=instance,
                ProyectoLogTypeID=proyecto_log_type,
                Comment=comment
            )

            crear_notificacion_rechazar_proyecto(instance, jefe_proyecto)
            eliminar_notificacion_proyecto_aprobacion(instance)
            eliminar_notificacion_proyecto_pendiente_aprobacion(instance)

        instance.ProyectoApprovalState = proyecto_approval_state
        instance.save()

        return instance


class CreateProyectoAseguradoraSerializer(serializers.ModelSerializer):
    ProyectoAseguradoraID = serializers.CharField(
        read_only=True,
        required=False,
        allow_null=True
    )
    AseguradoraID = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True
    )
    Aseguradora = serializers.CharField(
        source='AseguradoraID',
        read_only=True,
        required=False,
        allow_null=True
    )
    Amount = serializers.DecimalField(
        write_only=True,
        max_digits=10,
        decimal_places=2,
        allow_null=True,
        required=False
    )
    ExpirationDate = serializers.DateTimeField(
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = ProyectoAseguradora
        fields = ('ProyectoAseguradoraID', 'AseguradoraID',
                  'Aseguradora', 'Amount', 'ExpirationDate')


class CreateUserProyectoSerializer(serializers.ModelSerializer):
    UserID = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True,
        allow_blank=True
    )
    User = serializers.CharField(
        source='UserID',
        read_only=True,
        required=False
    )
    Proyecto = serializers.CharField(
        source='ProyectoID.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    UserProyectoType = serializers.CharField(
        source='UserProyectoTypeID',
        required=True,
        write_only=True
    )

    class Meta:
        model = UserProyecto
        fields = ('UserID', 'User', 'Proyecto', 'UserProyectoType')


class CreateProyectoContactInfoSerializer(serializers.ModelSerializer):
    Proyecto = serializers.CharField(
        source='ProyectoID.Name',
        read_only=True
    )
    ContactInfoTypeID = serializers.UUIDField(
        write_only=True,
        allow_null=True,
        required=False
    )
    ContactInfoType = serializers.CharField(
        source='ContactInfoTypeID',
        read_only=True,
        required=False,
        allow_null=True
    )
    Value = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = ProyectoContactInfo
        fields = ('Proyecto', 'ContactInfoTypeID', 'ContactInfoType', 'Value')


class CreateProyectoSerializer(serializers.ModelSerializer):
    InstitucionFinancieraID = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True
    )
    InstitucionFinanciera = serializers.CharField(
        source='InstitucionFinancieraID.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    InmobiliariaID = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True
    )
    Inmobiliaria = serializers.CharField(
        source='InmobiliariaID.RazonSocial',
        read_only=True,
        required=False,
        allow_null=True
    )
    ConstructoraID = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True
    )
    Constructora = serializers.CharField(
        source='ConstructoraID.RazonSocial',
        read_only=True,
        required=False,
        allow_null=True
    )
    ContactInfo = CreateProyectoContactInfoSerializer(
        many=True,
        required=False,
        allow_null=True
    )
    ComunaID = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True
    )
    Comuna = serializers.CharField(
        source='ComunaID.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    Provincia = serializers.CharField(
        source='ComunaID.ProvinciaID.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    Region = serializers.CharField(
        source='ComunaID.ProvinciaID.RegionID.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    ProyectoApprovalState = serializers.CharField(
        source='ProyectoApprovalState.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    PlanMediosState = serializers.CharField(
        source='PlanMediosState.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    BorradorPromesaState = serializers.CharField(
        source='BorradorPromesaState.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    IngresoComisionesState = serializers.CharField(
        source='IngresoComisionesState.Name',
        read_only=True,
        required=False,
        allow_null=True
    )
    EtapaStateID = serializers.UUIDField(
        required=False,
        allow_null=True
    )
    Aseguradora = CreateProyectoAseguradoraSerializer(
        source='ProyectoAseguradoraID',
        required=False,
        allow_null=True
    )
    UsersProyecto = CreateUserProyectoSerializer(
        source='UserProyecto',
        many=True,
        required=False,
        allow_null=True
    )
    Name = serializers.CharField(
        required=True,
        allow_null=True
    )
    Arquitecto = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )
    Symbol = serializers.CharField(
        required=False,
        allow_null=True
    )
    Address = serializers.CharField(
        required=False,
        allow_null=True
    )
    CotizacionDuration = serializers.CharField(
        required=False,
        allow_null=True
    )
    GuaranteeAmount = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    ContadoMontoPromesa = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    ContadoMontoCuotas = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    ContadoMontoEscrituraContado = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    ContadoAhorroPlus = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    ContadoAhorroPlusMaxDiscounts = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        required=False,
        allow_null=True
    )
    CreditoMontoPromesa = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    CreditoMontoCuotas = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    CreditoMontoEscrituraContado = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    CreditoAhorroPlus = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    CreditoAhorroPlusMaxDiscounts = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        required=False,
        allow_null=True
    )
    DiscountMaxPercent = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        required=False,
        allow_null=True
    )
    EntregaInmediata = serializers.BooleanField(required=False, write_only=True)

    class Meta:
        model = Proyecto
        fields = (
            'ProyectoID',
            'Name',
            'Symbol',
            'Address',
            'ContactInfo',
            'InstitucionFinancieraID',
            'InstitucionFinanciera',
            'InmobiliariaID',
            'Inmobiliaria',
            'ConstructoraID',
            'Constructora',
            'Provincia',
            'Comuna',
            'ComunaID',
            'Region',
            'ProyectoApprovalState',
            'PlanMediosState',
            'BorradorPromesaState',
            'IngresoComisionesState',
            'CotizacionDuration',
            'GuaranteeAmount',
            'ContadoMontoPromesa',
            'ContadoMontoCuotas',
            'ContadoMontoEscrituraContado',
            'ContadoAhorroPlus',
            'ContadoAhorroPlusMaxDiscounts',
            'CreditoMontoPromesa',
            'CreditoMontoCuotas',
            'CreditoMontoEscrituraContado',
            'CreditoAhorroPlus',
            'CreditoAhorroPlusMaxDiscounts',
            'DiscountMaxPercent',
            'UsersProyecto',
            'Aseguradora',
            'MoreThanOneEtapa',
            'EtapaStateID',
            'EntregaInmediata',
            'Arquitecto',
            'MaxCuotas',
            'MetasUf',
            'MetasPromesas'
        )

    def create(self, validated_data):
        current_user = return_current_user(self)

        contacts_info_data = validated_data.get('ContactInfo', []) if validated_data.get('ContactInfo') else []
        proyecto_users_data = validated_data.get('UsersProyecto', []) if validated_data.get('UsersProyecto') else []
        proyecto_aseguradora_data = validated_data.get('ProyectoAseguradoraID', []) if validated_data.get(
            'ProyectoAseguradoraID') else []
        institucion_financiera_id = validated_data.get('InstitucionFinancieraID')
        inmobiliaria_id = validated_data.get('InmobiliariaID')
        constructora_id = validated_data.get('ConstructoraID')
        comuna_id = validated_data.get('ComunaID')
        etapa_state_id = validated_data.get('EtapaStateID')
        symbol = validated_data.get('Symbol')

        institucion_financiera = InstitucionFinanciera.objects.get(
            InstitucionFinancieraID=institucion_financiera_id) if institucion_financiera_id else None
        inmobiliaria = Inmobiliaria.objects.get(InmobiliariaID=inmobiliaria_id) if inmobiliaria_id else None
        constructora = Constructora.objects.get(ConstructoraID=constructora_id) if constructora_id else None
        comuna = Comuna.objects.get(ComunaID=comuna_id) if comuna_id else None
        etapastate = EtapaState.objects.get(EtapaStateID=etapa_state_id) if etapa_state_id else None

        proyecto_approval_state = constants.PROYECTO_APPROVAL_STATE[0]

        plan_medios_state = constants.PLAN_MEDIOS_STATE[0]
        borrador_promesa_state = constants.BORRADOR_PROMESA_STATE[0]
        ingreso_comisiones_state = constants.INGRESO_COMISIONES_STATE[0]

        proyecto_approval = ProyectoApprovalState.objects.get(Name=proyecto_approval_state)
        plan_medios = PlanMediosState.objects.get(Name=plan_medios_state)
        borrador_promesa = BorradorPromesaState.objects.get(
            Name=borrador_promesa_state)
        ingreso_comisiones = IngresoComisionesState.objects.get(
            Name=ingreso_comisiones_state)

        instance = Proyecto.objects.create(
            Name=validated_data['Name'],
            Arquitecto=validated_data.get('Arquitecto',''),
            Symbol=symbol.upper() if symbol else symbol,
            Address=validated_data.get('Address'),
            InstitucionFinancieraID=institucion_financiera,
            ComunaID=comuna,
            InmobiliariaID=inmobiliaria,
            ConstructoraID=constructora,
            ProyectoApprovalState=proyecto_approval,
            CotizacionDuration=validated_data.get('CotizacionDuration', 0),
            GuaranteeAmount=validated_data.get('GuaranteeAmount', 0),
            ContadoMontoPromesa=validated_data.get('ContadoMontoPromesa', 20),
            ContadoMontoCuotas=validated_data.get('ContadoMontoCuotas', 20),
            ContadoMontoEscrituraContado=validated_data.get('ContadoMontoEscrituraContado', 20),
            ContadoAhorroPlus=validated_data.get('ContadoAhorroPlus', 20),
            ContadoAhorroPlusMaxDiscounts=validated_data.get('ContadoAhorroPlusMaxDiscounts', 1000),
            CreditoMontoPromesa=validated_data.get('CreditoMontoPromesa', 20),
            CreditoMontoCuotas=validated_data.get('CreditoMontoCuotas', 20),
            CreditoMontoEscrituraContado=validated_data.get('CreditoMontoEscrituraContado', 20),
            CreditoAhorroPlus=validated_data.get('CreditoAhorroPlus', 20),
            CreditoAhorroPlusMaxDiscounts=validated_data.get('CreditoAhorroPlusMaxDiscounts', 1000),
            DiscountMaxPercent=validated_data.get('DiscountMaxPercent', 100),
            MoreThanOneEtapa=validated_data.get('MoreThanOneEtapa', False),
            PlanMediosState=plan_medios,
            BorradorPromesaState=borrador_promesa,
            IngresoComisionesState=ingreso_comisiones,
            EtapaStateID=etapastate,
            EntregaInmediata=validated_data.get('EntregaInmediata', False),
            MetasUf=validated_data.get('MetasUf', 0),
            MetasPromesas=validated_data.get('MetasPromesas', 0),
            MaxCuotas=validated_data.get('MaxCuotas', 0)
        )
        if validated_data.get('EntregaInmediata') is True:
            notification_type = NotificationType.objects.get(
                Name=constants.NOTIFICATION_TYPE[3])
            notification = Notification.objects.create(
                NotificationTypeID=notification_type,
                TableID=instance.ProyectoID,
                Message="Project %s has been updated to immediately delivery" % instance.Name,
                RedirectRouteID=instance.ProyectoID
            )
            user_proyecto_type = UserProyectoType.objects.get(Name=constants.USER_PROYECTO_TYPE[3])
            for user in UserProyecto.objects.filter(ProyectoID=instance,
                                                    UserProyectoTypeID=user_proyecto_type):
                notification.UserID.add(user)

        for contact_info_data in contacts_info_data:
            contact_info_type = ContactInfoType.objects.get(
                ContactInfoTypeID=contact_info_data.get('ContactInfoTypeID'))
            ProyectoContactInfo.objects.create(
                ProyectoID=instance,
                ContactInfoTypeID=contact_info_type,
                Value=contact_info_data.get('Value'),
            )

        if proyecto_aseguradora_data and proyecto_aseguradora_data.get('AseguradoraID'):
            aseguradora = Aseguradora.objects.get(
                AseguradoraID=proyecto_aseguradora_data['AseguradoraID'])

            amount = proyecto_aseguradora_data['Amount']
            expiration_date = proyecto_aseguradora_data['ExpirationDate']

            proyecto_aseguradora = ProyectoAseguradora.objects.create(
                AseguradoraID=aseguradora,
                Amount=amount,
                ExpirationDate=expiration_date
            )
            instance.ProyectoAseguradoraID = proyecto_aseguradora
            instance.save()

        for proyecto_user_data in proyecto_users_data:
            if proyecto_user_data.get('UserID'):
                user_proyecto_type = UserProyectoType.objects.get(
                    Name=proyecto_user_data['UserProyectoType'])
                user_proyecto = User.objects.get(
                    UserID=proyecto_user_data['UserID'])
                if user_proyecto:
                    UserProyecto.objects.create(
                        UserID=user_proyecto,
                        ProyectoID=instance,
                        UserProyectoTypeID=user_proyecto_type
                    )

        # Creacion de Historial del Proyecto
        counter = CounterHistory.objects.create(
            ProyectoID=instance
        )

        proyecto_hist_data = dict(ProyectoID=instance.ProyectoID,
                                  Counter=counter.Count,
                                  Name=validated_data['Name'],
                                  Arquitecto=validated_data.get('Arquitecto',''),
                                  Symbol=symbol.upper() if symbol else symbol,
                                  Address=validated_data.get('Address'),
                                  InstitucionFinancieraID=institucion_financiera,
                                  ComunaID=comuna,
                                  InmobiliariaID=inmobiliaria,
                                  ConstructoraID=constructora,
                                  CotizacionDuration=validated_data.get('CotizacionDuration', 0),
                                  GuaranteeAmount=validated_data.get('GuaranteeAmount', 0),
                                  ContadoMontoPromesa=validated_data.get('ContadoMontoPromesa', 20),
                                  ContadoMontoCuotas=validated_data.get('ContadoMontoCuotas', 20),
                                  ContadoMontoEscrituraContado=validated_data.get('ContadoMontoEscrituraContado', 20),
                                  ContadoAhorroPlus=validated_data.get('ContadoAhorroPlus', 20),
                                  ContadoAhorroPlusMaxDiscounts=validated_data.get('ContadoAhorroPlusMaxDiscounts', 1000),
                                  CreditoMontoPromesa=validated_data.get('CreditoMontoPromesa', 20),
                                  CreditoMontoCuotas=validated_data.get('CreditoMontoCuotas', 20),
                                  CreditoMontoEscrituraContado=validated_data.get('CreditoMontoEscrituraContado', 20),
                                  CreditoAhorroPlus=validated_data.get('CreditoAhorroPlus', 20),
                                  CreditoAhorroPlusMaxDiscounts=validated_data.get('CreditoAhorroPlusMaxDiscounts', 1000),
                                  DiscountMaxPercent=validated_data.get('DiscountMaxPercent', 100),
                                  MoreThanOneEtapa=validated_data.get('MoreThanOneEtapa', False),
                                  PlanMediosState=plan_medios,
                                  BorradorPromesaState=borrador_promesa,
                                  IngresoComisionesState=ingreso_comisiones)
        null_fields = []
        for key, value in proyecto_hist_data.items():
            if value is None:
                null_fields.append(key)
        for field in null_fields:
            del proyecto_hist_data[field]

        proyecto_hist = HistoricalProyecto.objects.create(**proyecto_hist_data)

        for contact_info_data in contacts_info_data:
            contact_info_type = ContactInfoType.objects.get(
                ContactInfoTypeID=contact_info_data.get('ContactInfoTypeID'))

            HistoricalProyectoContactInfo.objects.create(
                ProyectoID=proyecto_hist,
                ContactInfoTypeID=contact_info_type,
                Value=contact_info_data.get('Value'),
            )

        if proyecto_aseguradora_data and proyecto_aseguradora_data.get('AseguradoraID') and validated_data.get(
                'EntregaInmediata') is True:
            aseguradora = Aseguradora.objects.get(
                AseguradoraID=proyecto_aseguradora_data['AseguradoraID'])

            amount = proyecto_aseguradora_data['Amount']
            expiration_date = proyecto_aseguradora_data['ExpirationDate']

            proyecto_aseguradora = HistoricalProyectoAseguradora.objects.create(
                AseguradoraID=aseguradora,
                Amount=amount,
                ExpirationDate=expiration_date
            )
            proyecto_hist.ProyectoAseguradoraID = proyecto_aseguradora
            proyecto_hist.save()
        else:
            proyecto_aseguradora = None

        for proyecto_user_data in proyecto_users_data:
            if proyecto_user_data.get('UserID'):
                user_proyecto_type = UserProyectoType.objects.get(
                    Name=proyecto_user_data['UserProyectoType'])
                user_proyecto = User.objects.get(
                    UserID=proyecto_user_data['UserID'])
                if user_proyecto:    
                    HistoricalUserProyecto.objects.create(
                        UserID=user_proyecto,
                        ProyectoID=proyecto_hist,
                        UserProyectoTypeID=user_proyecto_type
                    )
                    if proyecto_user_data['UserProyectoType'] in (constants.USER_PROYECTO_TYPE[5],
                                                                  constants.USER_PROYECTO_TYPE[6],
                                                                  constants.USER_PROYECTO_TYPE[7]):
                        notification_type = NotificationType.objects.get(
                            Name=constants.NOTIFICATION_TYPE[46])
                        notification = Notification.objects.create(
                            NotificationTypeID=notification_type,
                            TableID=instance.ProyectoID,
                            Message="You have been assigned to project %s to upload %s documents" % (instance.Name,
                                                                                                     proyecto_user_data[
                                                                                                         'UserProyectoType']),
                            RedirectRouteID=instance.ProyectoID
                        )
                        notification.UserID.add(user_proyecto)

        # Creacion de bitacora de proyecto
        proyecto_log_type = ProyectoLogType.objects.get(
            Name=constants.PROYECTO_LOG_TYPE[0])

        log = ProyectoLog.objects.create(
            UserID=current_user,
            ProyectoID=instance,
            ProyectoLogTypeID=proyecto_log_type,
            Counter=counter.Count
        )

        counter.Count += 1
        counter.save()

        # Datos para renderizar a pdf
        contactos = ProyectoContactInfo.objects.filter(ProyectoID=instance)
        usuarios = UserProyecto.objects.filter(ProyectoID=instance)

        context_dict = {
            'proyecto': instance,
            'contactos': contactos,
            'usuarios': usuarios,
            'date': log.Date
        }

        pdf = render_create_proyecto_to_pdf(context_dict)

        pdf_generated = ContentFile(pdf)
        pdf_generated.name = "Documento.pdf"

        log.ProyectoDetailDocument = pdf_generated
        log.save()

        # Crear contador del proyecto para el folio de las cotizaciones
        CounterFolio.objects.create(
            ProyectoID=instance
        )

        # Crear Notificaciones

        # Permisos
        permission_monitorea = Permission.objects.get(Name=constants.PERMISSIONS[14])
        permission_aprueba_inmuebles = Permission.objects.get(Name=constants.PERMISSIONS[19])

        # Tipo de Bitacora
        proyecto_log_type = ProyectoLogType.objects.get(
            Name=constants.PROYECTO_LOG_TYPE[0])

        # Tipos de usuarios
        creator = ProyectoLog.objects.get(
            ProyectoID=instance, ProyectoLogTypeID=proyecto_log_type)

        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])

        representante = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[0])

        vendedor = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[2])

        asistente_comercial = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[3])

        aprobador = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[4])

        # Usuarios
        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance, UserProyectoTypeID=jefe_proyecto_type)

        usuarios_monitorea_proyectos = User.objects.filter(
            RoleID__PermissionID=permission_monitorea
        )

        usuarios_aprueba_inmuebles = User.objects.filter(
            RoleID__PermissionID=permission_aprueba_inmuebles
        )

        representantes_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance, UserProyectoTypeID=representante)

        vendedores_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance, UserProyectoTypeID=vendedor)

        asistentes_comerciales_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance, UserProyectoTypeID=asistente_comercial)

        aprobadores_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance, UserProyectoTypeID=aprobador)

        # send email to project director
        if jefe_proyecto:
            base_url = "http://" + get_current_site(self.context.get('request')).domain
            file_url = base_url + settings.MEDIA_URL + log.ProyectoDetailDocument.name
            send_mail(message=file_url,
                      subject="You are assigned to '%s'" % instance.Name,
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[user.UserID.Email for user in jefe_proyecto],
                      html_message="Dear director, <br/><br/>The project {project_name} was created. "
                                   "As a director, you will have responsibilities to supervise this project.<br/><br/>"
                                   "Please review it at the link below<br/><br/>"
                                   "<a href='{file_url}'>FILE PDF</a>".format(project_name=instance.Name,
                                                                              file_url=file_url))
        # end sending email

        crear_notificacion_proyecto_sin_inmuebles(
            instance, current_user, jefe_proyecto, usuarios_monitorea_proyectos)

        crear_notificacion_proyecto_sin_borrador_promesa(
            instance, usuarios_aprueba_inmuebles)

        if institucion_financiera and institucion_financiera.Name == 'Pendiente':
            crear_notificacion_proyecto_sin_institucion_financiera(
                instance, current_user, jefe_proyecto, usuarios_monitorea_proyectos)

        if proyecto_aseguradora and proyecto_aseguradora.AseguradoraID.Name == 'Pendiente':
            crear_notificacion_proyecto_sin_aseguradora(
                instance, current_user, jefe_proyecto, usuarios_monitorea_proyectos)

        if constructora and constructora.RazonSocial == 'Pendiente':
            crear_notificacion_proyecto_sin_constructora(
                instance, current_user, jefe_proyecto, usuarios_monitorea_proyectos)

        if not representantes_proyecto.exists():
            crear_notificacion_proyecto_sin_representantes(
                instance, creator, jefe_proyecto, usuarios_monitorea_proyectos)

        if jefe_proyecto and not jefe_proyecto.exists():
            crear_notificacion_proyecto_sin_jefe_proyecto(
                instance, creator, usuarios_monitorea_proyectos)

        if vendedores_proyecto and not vendedores_proyecto.exists():
            crear_notificacion_proyecto_sin_vendedores(
                instance, creator, jefe_proyecto, usuarios_monitorea_proyectos)

        if asistentes_comerciales_proyecto and not asistentes_comerciales_proyecto.exists():
            crear_notificacion_proyecto_sin_asistentes_comerciales(
                instance, creator, jefe_proyecto, usuarios_monitorea_proyectos)

        if aprobadores_proyecto and not aprobadores_proyecto.exists():
            crear_notificacion_proyecto_sin_aprobador(
                instance, creator, jefe_proyecto, usuarios_monitorea_proyectos)

        # Crear Etapa por defecto
        if not validated_data.get('MoreThanOneEtapa') and validated_data.get('EtapaStateID'):
            etapa_state_id = validated_data.get('EtapaStateID')

            etapa_state = EtapaState.objects.get(
                EtapaStateID=etapa_state_id) if etapa_state_id else None

            Etapa.objects.create(
                Name=constants.DEFAULT_ETAPA_NAME,
                SalesStartDate=None,
                ProyectoID=instance,
                EtapaStateID=etapa_state
            )
        return instance


class UpdateProyectoSerializer(serializers.ModelSerializer):
    InstitucionFinancieraID = serializers.CharField(
        write_only=True,
        allow_null=True
    )
    InstitucionFinanciera = serializers.CharField(
        source='InstitucionFinancieraID.Name',
        read_only=True,
        allow_null=True
    )
    InmobiliariaID = serializers.CharField(
        write_only=True,
        allow_null=True
    )
    Inmobiliaria = serializers.CharField(
        source='InmobiliariaID.RazonSocial',
        read_only=True,
        allow_null=True
    )

    ConstructoraID = serializers.CharField(
        write_only=True,
        allow_null=True
    )
    Constructora = serializers.CharField(
        source='ConstructoraID.RazonSocial',
        read_only=True,
        allow_null=True
    )
    ContactInfo = CreateProyectoContactInfoSerializer(
        many=True,
        allow_null=True,
        required=False
    )
    ComunaID = serializers.CharField(
        write_only=True,
        allow_null=True
    )
    Comuna = serializers.CharField(
        source='ComunaID.Name',
        read_only=True,
        allow_null=True
    )
    Provincia = serializers.CharField(
        source='ComunaID.ProvinciaID.Name',
        read_only=True,
        allow_null=True
    )
    Region = serializers.CharField(
        source='ComunaID.ProvinciaID.RegionID.Name',
        read_only=True,
        allow_null=True
    )
    ProyectoApprovalState = serializers.CharField(
        source='ProyectoApprovalState.Name',
        read_only=True,
        allow_null=True
    )
    Aseguradora = CreateProyectoAseguradoraSerializer(
        source='ProyectoAseguradoraID',
        allow_null=True
    )
    UsersProyecto = CreateUserProyectoSerializer(
        source='UserProyecto',
        many=True,
        allow_null=True
    )
    Comment = serializers.CharField(
        allow_null=True,
        allow_blank=True,
        required=False
    )
    EtapaStateID = serializers.UUIDField(
        required=False,
        allow_null=True
    )
    Name = serializers.CharField(required=False)
    Arquitecto = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    Symbol = serializers.CharField(required=False, allow_null=True)
    Address = serializers.CharField(required=False, allow_null=True)
    CotizacionDuration = serializers.CharField(required=False, allow_null=True)
    GuaranteeAmount = serializers.IntegerField(required=False, allow_null=True)
    ContadoMontoPromesa = serializers.IntegerField(required=False, allow_null=True)
    ContadoMontoCuotas = serializers.IntegerField(required=False, allow_null=True)
    ContadoMontoEscrituraContado = serializers.IntegerField(required=False, allow_null=True)
    ContadoAhorroPlus = serializers.IntegerField(required=False, allow_null=True)
    ContadoAhorroPlusMaxDiscounts = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        required=False, allow_null=True
    )
    CreditoMontoPromesa = serializers.IntegerField(required=False, allow_null=True)
    CreditoMontoCuotas = serializers.IntegerField(required=False, allow_null=True)
    CreditoMontoEscrituraContado = serializers.IntegerField(required=False, allow_null=True)
    CreditoAhorroPlus = serializers.IntegerField(required=False, allow_null=True)
    CreditoAhorroPlusMaxDiscounts = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        required=False, allow_null=True
    )
    DiscountMaxPercent = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        required=False, allow_null=True
    )
    EntregaInmediata = serializers.BooleanField(required=False)

    class Meta:
        model = Proyecto
        fields = (
            'ProyectoID',
            'Name',
            'Arquitecto',
            'Symbol',
            'Address',
            'ContactInfo',
            'InstitucionFinancieraID',
            'InstitucionFinanciera',
            'InmobiliariaID',
            'Inmobiliaria',
            'ConstructoraID',
            'Constructora',
            'Provincia',
            'Comuna',
            'ComunaID',
            'Region',
            'ProyectoApprovalState',
            'CotizacionDuration',
            'GuaranteeAmount',
            'ContadoMontoPromesa',
            'ContadoMontoCuotas',
            'ContadoMontoEscrituraContado',
            'ContadoAhorroPlus',
            'ContadoAhorroPlusMaxDiscounts',
            'CreditoMontoPromesa',
            'CreditoMontoCuotas',
            'CreditoMontoEscrituraContado',
            'CreditoAhorroPlus',
            'CreditoAhorroPlusMaxDiscounts',
            'DiscountMaxPercent',
            'UsersProyecto',
            'Aseguradora',
            'MoreThanOneEtapa',
            'Comment',
            'EtapaStateID',
            'EntregaInmediata',
            'MetasUf',
            'MetasPromesas',
            'MaxCuotas',
        )

    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        contacts_info_data = validated_data.get('ContactInfo', False)
        proyecto_users_data = validated_data.get('UserProyecto', False)
        proyecto_aseguradora_data = validated_data.get('ProyectoAseguradoraID', False)
        institucion_financiera_id = validated_data.get('InstitucionFinancieraID', False)
        inmobiliaria_id = validated_data.get('InmobiliariaID', False)
        constructora_id = validated_data.get('ConstructoraID', False)
        comuna_id = validated_data.get('ComunaID', False)
        provincia_id = validated_data.get('ProvinciaID', False)
        region_id = validated_data.get('RegionID', False)
        comment = validated_data.get('Comment', False)
        symbol = validated_data.get('Symbol', False)
        arquitecto = validated_data.get('Arquitecto', False)
        etapa_state_id = validated_data.get('EtapaStateID', False)

        # Arreglos para guardar objetos antes del cambio
        contactos_not_changed = []
        users_not_changed = []

        institucion_financiera = InstitucionFinanciera.objects.get(InstitucionFinancieraID=institucion_financiera_id) if \
            institucion_financiera_id else None

        inmobiliaria = Inmobiliaria.objects.get(InmobiliariaID=inmobiliaria_id) if inmobiliaria_id else None
        constructora = Constructora.objects.get(
            ConstructoraID=constructora_id
        ) if constructora_id else None
        comuna = Comuna.objects.get(
            ComunaID=comuna_id
        ) if comuna_id else None
        provincia = Provincia.objects.get(ProvinciaID=provincia_id) if provincia_id else None
        region = Region.objects.get(RegionID=region_id) if region_id else None

        # Guardar Historial del Proyecto
        counter = CounterHistory.objects.get(ProyectoID=instance)
        etapastate = EtapaState.objects.get(EtapaStateID=etapa_state_id) if etapa_state_id else None

        proyecto_hist_data = dict(ProyectoID=instance.ProyectoID,
                                  Counter=counter.Count,
                                  Name=validated_data.get('Name', instance.Name),
                                  Arquitecto=arquitecto,
                                  Symbol=symbol.upper() if symbol else symbol,
                                  Address=validated_data.get('Address'),
                                  InstitucionFinancieraID=institucion_financiera,
                                  ComunaID=comuna,
                                  InmobiliariaID=inmobiliaria,
                                  ConstructoraID=constructora,
                                  CotizacionDuration=validated_data.get('CotizacionDuration', 0),
                                  GuaranteeAmount=validated_data.get('GuaranteeAmount', 0),
                                  ContadoMontoPromesa=validated_data.get('ContadoMontoPromesa', 20),
                                  ContadoMontoCuotas=validated_data.get('ContadoMontoCuotas', 20),
                                  ContadoMontoEscrituraContado=validated_data.get('ContadoMontoEscrituraContado', 20),
                                  CreditoMontoPromesa=validated_data.get('CreditoMontoPromesa', 20),
                                  ContadoAhorroPlus=validated_data.get('ContadoAhorroPlus', 20),
                                  ContadoAhorroPlusMaxDiscounts=validated_data.get('ContadoAhorroPlusMaxDiscounts', 1000),
                                  CreditoMontoCuotas=validated_data.get('CreditoMontoCuotas', 20),
                                  CreditoMontoEscrituraContado=validated_data.get('CreditoMontoEscrituraContado', 20),
                                  CreditoAhorroPlus=validated_data.get('CreditoAhorroPlus', 20),
                                  CreditoAhorroPlusMaxDiscounts=validated_data.get('CreditoAhorroPlusMaxDiscounts', 1000),
                                  DiscountMaxPercent=validated_data.get('DiscountMaxPercent', 100),
                                  MoreThanOneEtapa=validated_data.get('MoreThanOneEtapa', False),
                                  PlanMediosState=instance.PlanMediosState,
                                  BorradorPromesaState=instance.BorradorPromesaState,
                                  IngresoComisionesState=instance.IngresoComisionesState)
        proyecto_hist_data_validated = dict()
        for key, value in proyecto_hist_data.items():
            if value is not False:
                proyecto_hist_data_validated[key] = value
        proyecto_hist = HistoricalProyecto.objects.create(**proyecto_hist_data_validated)

        if contacts_info_data is not False:
            contactos_proyecto = ProyectoContactInfo.objects.filter(ProyectoID=instance)
            for contacto in contactos_proyecto:
                contactos_not_changed.append(contacto)
            if contactos_proyecto.exists():
                contactos_proyecto.delete()
            instance.ContactInfo.clear()
            if contacts_info_data is not None:
                for contact_info_data in contacts_info_data:
                    contact_info_type = ContactInfoType.objects.get(
                        ContactInfoTypeID=contact_info_data['ContactInfoTypeID'])
                    value = contact_info_data['Value']

                    ProyectoContactInfo.objects.create(
                        ProyectoID=instance,
                        ContactInfoTypeID=contact_info_type,
                        Value=value
                    )
                    HistoricalProyectoContactInfo.objects.create(
                        ProyectoID=proyecto_hist,
                        ContactInfoTypeID=contact_info_type,
                        Value=contact_info_data['Value'],
                    )

        proyecto_aseguradora = None
        aseguradora_proyecto = get_or_none(
            ProyectoAseguradora, aseguradora_proyecto=instance)
        aseguradora_not_changed = aseguradora_proyecto
        if proyecto_aseguradora_data is not False:
            # Se hace una copia para poder compararla con la nueva a crear
            if aseguradora_proyecto:
                aseguradora_proyecto.delete()
            if isinstance(proyecto_aseguradora_data, dict) and proyecto_aseguradora_data.get(
                    'AseguradoraID') and validated_data.get('EntregaInmediata', instance.EntregaInmediata) is True:
                aseguradora = Aseguradora.objects.get(
                    AseguradoraID=proyecto_aseguradora_data['AseguradoraID'])
                amount = proyecto_aseguradora_data['Amount']
                expiration_date = proyecto_aseguradora_data['ExpirationDate']

                proyecto_aseguradora = ProyectoAseguradora.objects.create(
                    AseguradoraID=aseguradora,
                    Amount=amount,
                    ExpirationDate=expiration_date
                )

                proyecto_aseguradora_hist = HistoricalProyectoAseguradora.objects.create(
                    AseguradoraID=aseguradora, Amount=amount, ExpirationDate=expiration_date)
                proyecto_hist.ProyectoAseguradoraID = proyecto_aseguradora_hist
                proyecto_hist.save()

        if proyecto_users_data is not False:
            users_proyecto = UserProyecto.objects.filter(ProyectoID=instance)
            for user in users_proyecto:
                users_not_changed.append(user)
            if users_proyecto.exists():
                users_proyecto.delete()
            instance.UserProyecto.clear()
            if proyecto_users_data is not None:
                for proyecto_user_data in proyecto_users_data:
                    if proyecto_user_data['UserID']:
                        user_proyecto_type = UserProyectoType.objects.get(
                            Name=proyecto_user_data['UserProyectoTypeID'])
                        user_proyecto = User.objects.get(
                            UserID=proyecto_user_data['UserID'])

                        UserProyecto.objects.create(
                            UserID=user_proyecto,
                            ProyectoID=instance,
                            UserProyectoTypeID=user_proyecto_type
                        )
                        HistoricalUserProyecto.objects.create(
                            UserID=user_proyecto,
                            ProyectoID=proyecto_hist,
                            UserProyectoTypeID=user_proyecto_type
                        )
                        if proyecto_user_data['UserProyectoTypeID'] in (constants.USER_PROYECTO_TYPE[5],
                                                                        constants.USER_PROYECTO_TYPE[6],
                                                                        constants.USER_PROYECTO_TYPE[7]):
                            notification_type = NotificationType.objects.get(
                                Name=constants.NOTIFICATION_TYPE[46])
                            notification = Notification.objects.create(
                                NotificationTypeID=notification_type,
                                TableID=instance.ProyectoID,
                                Message="You have been assigned to project %s to upload %s documents" % (instance.Name,
                                                                                                         proyecto_user_data[
                                                                                                             'UserProyectoTypeID']),
                                RedirectRouteID=instance.ProyectoID
                            )
                            notification.UserID.add(user_proyecto)

        # Crear/Eliminar Notificaciones

        # Permiso Monitorea Proyectos
        permission = Permission.objects.get(Name=constants.PERMISSIONS[14])

        # Tipo de Bitacora
        proyecto_log_type = ProyectoLogType.objects.get(
            Name=constants.PROYECTO_LOG_TYPE[0])

        # Tipos de usuarios
        creator = ProyectoLog.objects.get(
            ProyectoID=instance, ProyectoLogTypeID=proyecto_log_type)

        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])

        representante = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[0])

        vendedor = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[2])

        asistente_comercial = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[3])

        aprobador = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[4])

        # Usuarios
        jefe_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance, UserProyectoTypeID=jefe_proyecto_type)

        usuarios_monitorea_proyectos = User.objects.filter(
            RoleID__PermissionID=permission
        )
        representantes_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance, UserProyectoTypeID=representante)

        vendedores_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance, UserProyectoTypeID=vendedor)

        asistentes_comerciales_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance, UserProyectoTypeID=asistente_comercial)

        aprobadores_proyecto = UserProyecto.objects.filter(
            ProyectoID=instance, UserProyectoTypeID=aprobador)

        if representantes_proyecto.exists():
            eliminar_notificacion_proyecto_sin_representante(instance)
        else:
            crear_notificacion_proyecto_sin_representantes(
                instance, creator, jefe_proyecto, usuarios_monitorea_proyectos)

        if jefe_proyecto.exists():
            eliminar_notificacion_proyecto_sin_jefe_proyecto(instance)
        else:
            crear_notificacion_proyecto_sin_jefe_proyecto(
                instance, creator, usuarios_monitorea_proyectos)

        if vendedores_proyecto.exists():
            eliminar_notificacion_proyecto_sin_vendedores(instance)
        else:
            crear_notificacion_proyecto_sin_vendedores(
                instance, creator, jefe_proyecto, usuarios_monitorea_proyectos)

        if asistentes_comerciales_proyecto.exists():
            eliminar_notificacion_proyecto_sin_asistentes_comerciales(instance)
        else:
            crear_notificacion_proyecto_sin_asistentes_comerciales(
                instance, creator, jefe_proyecto, usuarios_monitorea_proyectos)

        if aprobadores_proyecto.exists():
            eliminar_notificacion_proyecto_sin_aprobador(instance)
        else:
            crear_notificacion_proyecto_sin_aprobador(
                instance, creator, jefe_proyecto, usuarios_monitorea_proyectos)

        if institucion_financiera and institucion_financiera.Name == 'Pendiente':
            crear_notificacion_proyecto_sin_institucion_financiera(
                instance, current_user, jefe_proyecto, usuarios_monitorea_proyectos)
        else:
            eliminar_notificacion_proyecto_sin_institucion_financiera(instance)

        if proyecto_aseguradora and proyecto_aseguradora.AseguradoraID.Name == 'Pendiente':
            crear_notificacion_proyecto_sin_aseguradora(
                instance, current_user, jefe_proyecto, usuarios_monitorea_proyectos)
        else:
            eliminar_notificacion_proyecto_sin_aseguradora(instance)

        if constructora and constructora.RazonSocial == 'Pendiente':
            crear_notificacion_proyecto_sin_constructora(
                instance, current_user, jefe_proyecto, usuarios_monitorea_proyectos)
        else:
            eliminar_notificacion_proyecto_sin_constructora(instance)

        # Creacion de bitacora de proyecto
        proyecto_log_type = ProyectoLogType.objects.get(
            Name=constants.PROYECTO_LOG_TYPE[2])

        log = ProyectoLog.objects.create(
            UserID=current_user,
            ProyectoID=instance,
            ProyectoLogTypeID=proyecto_log_type,
            Counter=counter.Count,
            Comment=comment
        )

        counter.Count += 1
        counter.save()

        # Datos para renderizar a pdf
        contactos_nuevos = ProyectoContactInfo.objects.filter(
            ProyectoID=instance)
        usuarios_nuevos = UserProyecto.objects.filter(
            ProyectoID=instance)

        context_dict = {
            'proyecto': instance,
            'datos_modificados': validated_data,
            'institucion_financiera_nueva': institucion_financiera,
            'inmobiliaria_nueva': inmobiliaria,
            'constructora_nueva': constructora,
            'comuna_nueva': comuna,
            'contactos': contactos_not_changed,
            'contactos_nuevos': contactos_nuevos,
            'aseguradora': aseguradora_not_changed,
            'aseguradora_nueva': proyecto_aseguradora,
            'usuarios': users_not_changed,
            'usuarios_nuevos': usuarios_nuevos,
            'date': log.Date
        }

        pdf = render_update_proyecto_to_pdf(context_dict)

        pdf_generated = ContentFile(pdf)
        pdf_generated.name = "Documento.pdf"

        log.ProyectoDetailDocument = pdf_generated

        if 'Name' in validated_data:
            instance.Name = validated_data.get('Name')
        if arquitecto is not False:
            instance.Arquitecto = arquitecto   
        if symbol is not False:
            instance.Symbol = symbol.upper() if symbol else symbol
        if 'Address' in validated_data:
            instance.Address = validated_data.get('Address')
        if institucion_financiera_id is not False:
            instance.InstitucionFinancieraID = institucion_financiera
        if comuna_id is not False:
            instance.ComunaID = comuna
        if provincia_id is not False:
            instance.ProvincaID = provincia
        if region_id is not False:
            instance.RegionID = region
        if inmobiliaria_id is not False:
            instance.InmobiliariaID = inmobiliaria
        if constructora_id is not False:
            instance.ConstructoraID = constructora
        if proyecto_aseguradora_data is not False:
            instance.ProyectoAseguradoraID = proyecto_aseguradora
        if 'CotizacionDuration' in validated_data:
            instance.CotizacionDuration = validated_data.get('CotizacionDuration')
        if 'GuaranteeAmount' in validated_data:
            instance.GuaranteeAmount = validated_data.get('GuaranteeAmount')
        if 'ContadoMontoPromesa' in validated_data:
            instance.ContadoMontoPromesa = validated_data.get('ContadoMontoPromesa')
        if 'ContadoMontoCuotas' in validated_data:
            instance.ContadoMontoCuotas = validated_data.get('ContadoMontoCuotas')
        if 'ContadoMontoEscrituraContado' in validated_data:
            instance.ContadoMontoEscrituraContado = validated_data.get('ContadoMontoEscrituraContado')
        if 'ContadoAhorroPlus' in validated_data:
            instance.ContadoAhorroPlus = validated_data.get('ContadoAhorroPlus')
        if 'ContadoAhorroPlusMaxDiscounts' in validated_data:
            instance.ContadoAhorroPlusMaxDiscounts = validated_data.get('ContadoAhorroPlusMaxDiscounts')
        if 'CreditoMontoPromesa' in validated_data:
            instance.CreditoMontoPromesa = validated_data.get('CreditoMontoPromesa')
        if 'CreditoMontoCuotas' in validated_data:
            instance.CreditoMontoCuotas = validated_data.get('CreditoMontoCuotas')
        if 'CreditoMontoEscrituraContado' in validated_data:
            instance.CreditoMontoEscrituraContado = validated_data.get('CreditoMontoEscrituraContado')
        if 'CreditoAhorroPlus' in validated_data:
            instance.CreditoAhorroPlus = validated_data.get('CreditoAhorroPlus')
        if 'CreditoAhorroPlusMaxDiscounts' in validated_data:
            instance.CreditoAhorroPlusMaxDiscounts = validated_data.get('CreditoAhorroPlusMaxDiscounts')
        if 'DiscountMaxPercent' in validated_data:
            instance.DiscountMaxPercent = validated_data.get('DiscountMaxPercent')
        if 'MoreThanOneEtapa' in validated_data:
            instance.MoreThanOneEtapa = validated_data.get('MoreThanOneEtapa')
        if etapa_state_id is not False:
            instance.EtapaStateID = etapastate
        if 'EntregaInmediata' in validated_data:
            instance.EntregaInmediata = validated_data.get('EntregaInmediata')
        if 'MetasUf' in validated_data:
            instance.MetasUf = validated_data.get('MetasUf', 0)
        if 'MetasPromesas' in validated_data:
            instance.MetasPromesas = validated_data.get('MetasPromesas', 0)
        if 'MaxCuotas' in validated_data:
            instance.MaxCuotas = validated_data.get('MaxCuotas', 0)

        instance.save()
        log.save()
        if 'EntregaInmediata' in validated_data and validated_data[
            'EntregaInmediata'] is True and instance.EntregaInmediata is False:
            notification_type = NotificationType.objects.get(
                Name=constants.NOTIFICATION_TYPE[3])
            notification = Notification.objects.create(
                NotificationTypeID=notification_type,
                TableID=instance.ProyectoID,
                Message="Project %s has been updated to immediately delivery" % instance.Name,
                RedirectRouteID=instance.ProyectoID
            )
            user_proyecto_type = UserProyectoType.objects.get(Name=constants.USER_PROYECTO_TYPE[3])
            for user in UserProyecto.objects.filter(ProyectoID=instance,
                                                    UserProyectoTypeID=user_proyecto_type):
                notification.UserID.add(user)
        if validated_data.get('EntregaInmediata') is False and instance.ProyectoAseguradoraID is not None:
            instance.ProyectoAseguradoraID.delete()
        return instance


class UpdateProyectoLogTypeSerializer(serializers.ModelSerializer):
    Value = serializers.IntegerField(
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = ProyectoLogType
        fields = ('MaximunDays', 'Value')

    def update(self, instance, validated_data):
        maximun_days = validated_data['Value']

        instance.MaximunDays = maximun_days
        instance.save()

        return instance


class SendProyectoLegalSerializer(serializers.ModelSerializer):
    ProyectoApprovalState = serializers.CharField(
        source='ProyectoApprovalState.Name',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Proyecto
        fields = ('ProyectoApprovalState',)

    def update(self, instance, validated_data):
        verify_data_proyecto(instance)

        if instance.BorradorPromesaState.Name == constants.BORRADOR_PROMESA_STATE[0]:
            raise CustomValidation(
                "Falta agregar borrador promesa",
                status_code=status.HTTP_409_CONFLICT)

        if instance.ProyectoApprovalState.Name == constants.PROYECTO_APPROVAL_STATE[2]:
            raise CustomValidation(
                "Proyecto ya fue aprobado por legal",
                status_code=status.HTTP_409_CONFLICT)

        if instance.ProyectoApprovalState.Name == constants.PROYECTO_APPROVAL_STATE[3]:
            raise CustomValidation(
                "Proyecto ya está aprobado",
                status_code=status.HTTP_409_CONFLICT)

        # Crear notificacion a usuarios aprueba proyectos
        permission = Permission.objects.get(Name=constants.PERMISSIONS[19])

        usuarios_aprueba_inmuebles = User.objects.filter(
            RoleID__PermissionID=permission
        )

        if crear_notificacion_usuarios_aprueba_inmuebles(instance, usuarios_aprueba_inmuebles):
            raise CustomValidation(
                "Proyecto ya está en espera de aprobación",
                status_code=status.HTTP_409_CONFLICT)
        else:
            # Tipos de Usuarios
            jefe_proyecto_type = UserProyectoType.objects.get(
                Name=constants.USER_PROYECTO_TYPE[1])

            # Usuarios
            jefe_proyecto = UserProyecto.objects.filter(
                ProyectoID=instance, UserProyectoTypeID=jefe_proyecto_type)

            area_approve = constants.AREA_APPROVE[0]

            crear_notificacion_proyecto_pendiente_aprobacion(
                instance, jefe_proyecto, area_approve)

        approval_state = ProyectoApprovalState.objects.get(Name=constants.PROYECTO_APPROVAL_STATE[1])
        instance.ProyectoApprovalState = approval_state
        instance.save()

        return instance


class SendProyectoGerenciaSerializer(serializers.ModelSerializer):
    ProyectoApprovalState = serializers.CharField(
        source='ProyectoApprovalState.Name',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Proyecto
        fields = ('ProyectoApprovalState',)

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        if instance.ProyectoApprovalState.Name == constants.PROYECTO_APPROVAL_STATE[1]:
            raise CustomValidation(
                "Proyecto debe ser aprobado por legal",
                status_code=status.HTTP_409_CONFLICT)

        if instance.ProyectoApprovalState.Name == constants.PROYECTO_APPROVAL_STATE[3]:
            raise CustomValidation(
                "Proyecto ya fue aprobado por gerencia",
                status_code=status.HTTP_409_CONFLICT)

        # if instance.PlanMediosState.Name == constants.PLAN_MEDIOS_STATE[0]:
        #     raise CustomValidation(
        #         "Falta agregar plan de medios",
        #         status_code=status.HTTP_409_CONFLICT)
        #
        # if instance.BorradorPromesaState.Name == constants.BORRADOR_PROMESA_STATE[0]:
        #     raise CustomValidation(
        #         "Falta agregar borrador promesa",
        #         status_code=status.HTTP_409_CONFLICT)

        # if instance.IngresoComisionesState.Name == constants.INGRESO_COMISIONES_STATE[0]:
        #     raise CustomValidation(
        #         "Falta ingresar comisiones",
        #         status_code=status.HTTP_409_CONFLICT)

        verify_data_proyecto(instance)

        # Crear notificacion a usuarios aprueba proyectos
        permission = Permission.objects.get(Name=constants.PERMISSIONS[14])

        usuarios_monitorea_proyectos = User.objects.filter(
            RoleID__PermissionID=permission
        )

        if crear_notificacion_usuarios_monitorea_proyectos(instance, usuarios_monitorea_proyectos):
            raise CustomValidation(
                "Proyecto ya está en espera de aprobación",
                status_code=status.HTTP_409_CONFLICT)
        else:
            area_approve = constants.AREA_APPROVE[1]
            crear_notificacion_proyecto_pendiente_aprobacion(
                instance, current_user, area_approve)

        return instance


class AddBorradorPromesaSerializer(serializers.ModelSerializer):
    BorradorPromesaState = serializers.CharField(
        source='BorradorPromesaState.Name',
        required=False,
        allow_null=True
    )
    Resolution = serializers.BooleanField(
        write_only=True,
        required=False
    )

    class Meta:
        model = Proyecto
        fields = ('BorradorPromesaState', 'Resolution')

    def update(self, instance, validated_data):
        resolution = validated_data.pop('Resolution')

        if resolution:
            borrador_promesa = BorradorPromesaState.objects.get(Name=constants.BORRADOR_PROMESA_STATE[1])
            instance.BorradorPromesaState = borrador_promesa
            eliminar_notificacion_borrador_promesa(instance)
        instance.save()
        return instance


class UploadFileSerialier(serializers.ModelSerializer):
    Documents = ProjectDocumentSerializer(read_only=True)

    def validate_file_extension(self, key, extensions=None):
        # In case not update document
        if key not in self.initial_data:
            return False
        # In case remove document
        file = self.initial_data.get(key)
        if (key in self.initial_data and not file) or file == 'null':
            return None
        # In case update document
        if file == constants.FILE_NON_EXISTED or not extensions or any([file.name.endswith(ext) for ext in extensions]):
            return file
        raise ValidationError("{filename} is not in valid type. Expected {extensions}".format(filename=file.name,
                                                                                              extensions=", ".join(
                                                                                                  extensions)))

    def create_document(self, file, file_type, project_id, no_existed=False):
        document = dict(DocumentType=file_type,
                        Poster=return_current_user(self),
                        ProjectID=project_id,
                        NoExisted=no_existed)
        if file:
            document['Document'] = file
        return ProjectDocument.objects.create(**document)

    @staticmethod
    def remove_old_document(instance, document_type):
        docs = ProjectDocument.objects.filter(ProjectID=instance.ProyectoID, DocumentType=document_type)
        for doc in docs:
            doc.delete()

    def add_document(self, instance, file, doc_type):
        # Mark document as non existed
        # Does not update document
        if file is False:
            return False
        # Remove document
        elif file is None:
            self.remove_old_document(instance, doc_type)
        # Update document
        else:
            no_existed = False
            if file == constants.FILE_NON_EXISTED:
                file = None
                no_existed = True
            self.remove_old_document(instance, doc_type)
            instance.Documents.add(self.create_document(file, doc_type, instance.ProyectoID, no_existed=no_existed))
        return True

    def get_excel_file(self, key):
        return self.validate_file_extension(key, ['xlsx', 'xls'])

    def get_pdf_file(self, key):
        return self.validate_file_extension(key, ['pdf'])

    def get_word_file(self, key):
        return self.validate_file_extension(key, ['doc', 'docx'])

    def get_file(self, key):
        return self.validate_file_extension(key)

    @staticmethod
    def get_all_uploaded_documents(instance):
        document_types = set()
        for document in ProjectDocument.objects.filter(ProjectID=instance.ProyectoID):
            document_types.add(document.DocumentType)
        return document_types

    def reset_state(self, instance):
        marketing_types = set(constants.MarketingDocumentTypes.values())
        legal_types = set(constants.LegalDocumentTypes.values())
        uploaded_types = self.get_all_uploaded_documents(instance)

        if marketing_types.issubset(uploaded_types):
            instance.PlanMediosState = PlanMediosState.objects.get(Name=constants.PLAN_MEDIOS_STATE[1])
        else:
            instance.PlanMediosState = PlanMediosState.objects.get(Name=constants.PLAN_MEDIOS_STATE[0])
        if legal_types.issubset(uploaded_types):
            instance.BorradorPromesaState = BorradorPromesaState.objects.get(Name=constants.BORRADOR_PROMESA_STATE[1])
        else:
            instance.BorradorPromesaState = BorradorPromesaState.objects.get(Name=constants.BORRADOR_PROMESA_STATE[0])

        instance.save()

    @staticmethod
    def create_notification(instance, **kwargs):
        doc_type = kwargs.get('doc_type')
        # Usuarios
        jefe_proyecto_type = UserProyectoType.objects.get(Name=constants.USER_PROYECTO_TYPE[1])
        jefe_proyecto = UserProyecto.objects.filter(ProyectoID=instance, UserProyectoTypeID=jefe_proyecto_type)
        if jefe_proyecto.exists():
            notification_type = NotificationType.objects.get(
                Name=constants.NOTIFICATION_TYPE[46])
            notification = Notification.objects.create(
                NotificationTypeID=notification_type,
                TableID=instance.ProyectoID,
                Message="Proyecto %s has updated document %s" % (instance.Name, doc_type),
                RedirectRouteID=instance.ProyectoID
            )
            for user in jefe_proyecto:
                notification.UserID.add(user.UserID)
            return jefe_proyecto
        return None

    @staticmethod
    def create_project_log(instance, current_user):
        counter = CounterHistory.objects.get(
            ProyectoID=instance
        )
        proyecto_log_type = ProyectoLogType.objects.get(
            Name=constants.PROYECTO_LOG_TYPE[2])

        log = ProyectoLog.objects.create(
            UserID=current_user,
            ProyectoID=instance,
            ProyectoLogTypeID=proyecto_log_type,
            Counter=counter.Count
        )
        counter.Count += 1
        counter.save()

        # Datos para renderizar a pdf
        contactos = ProyectoContactInfo.objects.filter(ProyectoID=instance)
        usuarios = UserProyecto.objects.filter(ProyectoID=instance)

        context_dict = {
            'proyecto': instance,
            'contactos': contactos,
            'usuarios': usuarios,
            'date': log.Date
        }

        pdf = render_create_proyecto_to_pdf(context_dict)

        pdf_generated = ContentFile(pdf)
        pdf_generated.name = "Documento.pdf"
        log.ProyectoDetailDocument = pdf_generated
        log.save()
        return log


class UpdateProyectoMarketingSerializer(UploadFileSerialier):
    class Meta:
        model = Proyecto
        fields = ()

    def upload(self, instance, **kwargs):
        marketing_excel = self.get_excel_file(constants.MarketingDocumentTypes.MARKETING_EXCEL)
        self.add_document(instance, marketing_excel, constants.MarketingDocumentTypes.MARKETING_EXCEL)

        marketing_pdf = self.get_pdf_file(constants.MarketingDocumentTypes.MARKETING_PDF)
        self.add_document(instance, marketing_pdf, constants.MarketingDocumentTypes.MARKETING_PDF)

        if marketing_excel or marketing_pdf:
            current_user = return_current_user(self)
            log = self.create_project_log(instance, current_user)
            project_director = self.create_notification(instance, doc_type='marketing')
            if project_director:
                base_url = "http://" + get_current_site(self.context.get('request')).domain
                file_url = base_url + settings.MEDIA_URL + log.ProyectoDetailDocument.name
                send_mail(message=file_url,
                          subject="Uploaded Marketing Document",
                          from_email=settings.EMAIL_HOST_USER,
                          recipient_list=[user.UserID.Email for user in project_director],
                          html_message="<a href='%s'>PDF FILE</a>" % file_url)
        instance.save()
        self.reset_state(instance)
        return instance


class UpdateProyectoLegalSerializer(UploadFileSerialier):
    class Meta:
        model = Proyecto
        fields = ()

    def upload(self, instance):
        counter_word = self.get_word_file(constants.LegalDocumentTypes.COUNTER_WORD)
        self.add_document(instance, counter_word, constants.LegalDocumentTypes.COUNTER_WORD)

        counter_pdf = self.get_pdf_file(constants.LegalDocumentTypes.COUNTER_PDF)
        self.add_document(instance, counter_pdf, constants.LegalDocumentTypes.COUNTER_PDF)

        credit_word = self.get_word_file(constants.LegalDocumentTypes.CREDIT_WORD)
        self.add_document(instance, credit_word, constants.LegalDocumentTypes.CREDIT_WORD)

        credit_pdf = self.get_pdf_file(constants.LegalDocumentTypes.CREDIT_PDF)
        self.add_document(instance, credit_pdf, constants.LegalDocumentTypes.CREDIT_PDF)

        company_word = self.get_word_file(constants.LegalDocumentTypes.COMPANY_WORD)
        self.add_document(instance, company_word, constants.LegalDocumentTypes.COMPANY_WORD)

        company_pdf = self.get_pdf_file(constants.LegalDocumentTypes.COMPANY_PDF)
        self.add_document(instance, company_pdf, constants.LegalDocumentTypes.COMPANY_PDF)

        brokerage_contract = self.get_file(constants.LegalDocumentTypes.BROKERAGE_CONTRACT)
        self.add_document(instance, brokerage_contract, constants.LegalDocumentTypes.BROKERAGE_CONTRACT)

        domain_certificate = self.get_file(constants.LegalDocumentTypes.DOMAIN_CERTIFICATE)
        self.add_document(instance, domain_certificate, constants.LegalDocumentTypes.DOMAIN_CERTIFICATE)

        company_deed = self.get_file(constants.LegalDocumentTypes.COMPANY_DEED)
        self.add_document(instance, company_deed, constants.LegalDocumentTypes.COMPANY_DEED)

        approved_price_list = self.get_file(constants.LegalDocumentTypes.APPROVED_PRICE_LIST)
        self.add_document(instance, approved_price_list, constants.LegalDocumentTypes.APPROVED_PRICE_LIST)

        title_folder = self.get_file(constants.LegalDocumentTypes.TITLE_FOLDER)
        self.add_document(instance, title_folder, constants.LegalDocumentTypes.TITLE_FOLDER)

        if counter_word or counter_pdf or credit_word or credit_pdf or company_word or company_pdf or \
                brokerage_contract or domain_certificate or company_deed or approved_price_list or title_folder:
            current_user = return_current_user(self)
            log = self.create_project_log(instance, current_user)
            project_director = self.create_notification(instance, doc_type='legal')
            if project_director:
                base_url = "http://" + get_current_site(self.context.get('request')).domain
                file_url = base_url + settings.MEDIA_URL + log.ProyectoDetailDocument.name
                send_mail(message=file_url,
                          subject="Uploaded Legal Document",
                          from_email=settings.EMAIL_HOST_USER,
                          recipient_list=[user.UserID.Email for user in project_director],
                          html_message="<a href='%s'>PDF FILE</a>" % file_url)
        instance.save()
        self.reset_state(instance)
        return instance


class ReviewProjectDocumentSerializer(UploadFileSerialier):
    Documentos = ProjectDocumentSerializer(read_only=True)

    class Meta:
        model = ProjectDocument
        fields = (
            'Documentos',
        )

    def create_notification(self, instance, **kwargs):
        initial_data = kwargs.get('initial_data')
        doc_type = kwargs.get('doc_type')
        document = kwargs.get('document')

        if initial_data.get(doc_type) == constants.DocumentState.CONFIRMED:
            notification_type = NotificationType.objects.get(
                Name=constants.NOTIFICATION_TYPE[44])
        else:
            notification_type = NotificationType.objects.get(
                Name=constants.NOTIFICATION_TYPE[45])
        notification = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=instance.ProyectoID,
            Message="Document %s has been %s by %s" % (doc_type,
                                                       initial_data.get(doc_type),
                                                       return_current_user(self).Name),
            RedirectRouteID=instance.ProyectoID
        )
        notification.UserID.add(document.Poster)

    def review(self, instance, initial_data):
        for doc_type in initial_data:
            data = "rejected" if initial_data.get(doc_type).startswith("rejected") else initial_data.get(doc_type)
            try:
                if data not in constants.DocumentState.values():
                    raise ValidationError(
                        "Status %s for document %s is not valid" % (initial_data.get(doc_type), doc_type))
                document = ProjectDocument.objects.get(ProjectID=instance.ProyectoID, DocumentType=doc_type)
                document.State = initial_data.get(doc_type)
                document.save()
                self.create_notification(instance, document=document, initial_data=initial_data, doc_type=doc_type)
            except ProjectDocument.DoesNotExist:
                raise ValidationError("Can not %s non-exist document: %s" % (initial_data.get(doc_type), doc_type))
        return instance


class RestrictionSerializer(object):
    def __init__(self, restriction):
        self.restriction = restriction

    def to_dict(self):
        data = dict(InmuebleBID=self.restriction.InmuebleBID.InmuebleID,
                    Inmueble=self.restriction.InmuebleBID.InmuebleTypeID.Name + ' ' + str(self.restriction.InmuebleBID.Number),
                    InmuebleInmuebleTypeID=self.restriction.InmuebleInmuebleTypeID.InmuebleInmuebleTypeID,
                    InmuebleInmuebleType=self.restriction.InmuebleInmuebleTypeID.Name)
        return data


class ProyectoRestrictionSerializer(object):
    def __init__(self, restrictions):
        self.restrictions = restrictions
        self.restrictions_grouped = dict()

    def to_dict(self):
        self.make_restrictions_grouped()
        aid_set = list(set([restriction.InmuebleAID for restriction in self.restrictions]))
        data = list()
        for aid in aid_set:
            tmp = dict(InmuebleAID=aid.InmuebleID,
                       Inmueble=aid.InmuebleTypeID.Name + ' ' + str(aid.Number),
                       Restrictions=self.restrictions_grouped.get(aid.InmuebleID, []))
            data.append(tmp)
        return data

    def make_restrictions_grouped(self):
        if not self.restrictions_grouped:
            for restriction in self.restrictions:
                restriction_data = RestrictionSerializer(restriction).to_dict()
                self.restrictions_grouped.setdefault(restriction.InmuebleAID.InmuebleID, []).append(restriction_data)
        return self.restrictions_grouped
