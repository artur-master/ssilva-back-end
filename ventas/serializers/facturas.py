from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common import constants
from common.generate_pdf import (
    render_create_factura_to_pdf,
    render_create_nota_credito_to_pdf, render_create_proyecto_to_pdf)
from common.models import Notification, NotificationType
from common.notifications import eliminar_notificacion_proyecto_sin_jefe_proyecto, crear_notificacion_proyecto_sin_jefe_proyecto
from common.services import return_current_user
from empresas_and_proyectos.models.proyectos import Proyecto, UserProyecto, ProyectoContactInfo, UserProyectoType
from empresas_and_proyectos.models.proyectos_logs import ProyectoLog, ProyectoLogType
from empresas_and_proyectos.models.states import IngresoComisionesState
from history.models import CounterHistory
from sgi_web_back_project import settings
from users.models import User, Permission
from ventas.models.facturas import ComisionInmobiliaria, FacturaInmueble, Factura
from ventas.serializers.cotizaciones import ListCotizacionesInmueblesSerializer


class CreateComisionesSerializer(serializers.ModelSerializer):
    ProyectoID = serializers.CharField()
    PromesaFirmada = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        required=False
    )
    EscrituraFirmada = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        required=False
    )
    CierreGestion = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        required=False
    )

    class Meta:
        model = ComisionInmobiliaria
        fields = ('ProyectoID', 'PromesaFirmada', 'EscrituraFirmada',
                  'CierreGestion')

    @staticmethod
    def create_notification(project_instance, **kwargs):
        notification_type = kwargs.get('notification_type')
        jefe_proyecto_type = UserProyectoType.objects.get(Name=constants.USER_PROYECTO_TYPE[1])
        jefe_proyecto = UserProyecto.objects.filter(ProyectoID=project_instance, UserProyectoTypeID=jefe_proyecto_type)

        if jefe_proyecto.exists():
            notification_type = NotificationType.objects.get(Name=notification_type)
            notification = Notification.objects.create(
                NotificationTypeID=notification_type,
                TableID=project_instance.ProyectoID,
                Message="Proyecto %s has updated comisiones" % project_instance.Name,
                RedirectRouteID=project_instance.ProyectoID
            )
            for user in jefe_proyecto:
                notification.UserID.add(user.UserID)
            return jefe_proyecto
        return None

    @staticmethod
    def create_project_log(instance, current_user):
        try:
            counter = CounterHistory.objects.get(ProyectoID=instance)
            counter.Count += 1
            counter.save()
        except CounterHistory.DoesNotExist:
            counter = CounterHistory.objects.create(ProyectoID=instance)
        except CounterHistory.MultipleObjectsReturned:
            for history in CounterHistory.objects.filter(ProyectoID=instance):
                history.delete()
            counter = CounterHistory.objects.create(ProyectoID=instance)

        proyecto_log_type = ProyectoLogType.objects.get(
            Name=constants.PROYECTO_LOG_TYPE[2])

        log = ProyectoLog.objects.create(
            UserID=current_user,
            ProyectoID=instance,
            ProyectoLogTypeID=proyecto_log_type,
            Counter=counter.Count - 1
        )

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

    def create(self, validated_data):
        proyecto_id = validated_data.get('ProyectoID')
        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        promesa_firmada = validated_data.get('PromesaFirmada', False)
        escritura_firmada = validated_data.get('EscrituraFirmada', False)
        cierre_gestion = validated_data.get('CierreGestion', False)

        try:
            comisiones = ComisionInmobiliaria.objects.get(ProyectoID=proyecto)
            if promesa_firmada is not False:
                comisiones.PromesaFirmada = promesa_firmada
            if escritura_firmada is not False:
                comisiones.EscrituraFirmada = escritura_firmada
            if cierre_gestion is not False:
                comisiones.CierreGestion = cierre_gestion
            comisiones.save()
        except ComisionInmobiliaria.DoesNotExist:
            comisiones = ComisionInmobiliaria.objects.create(
                ProyectoID=proyecto,
                PromesaFirmada=promesa_firmada,
                EscrituraFirmada=escritura_firmada,
                CierreGestion=cierre_gestion,
            )
        except ComisionInmobiliaria.MultipleObjectsReturned:
            for comission in ComisionInmobiliaria.objects.filter(ProyectoID=proyecto):
                comission.delete()
            comisiones = ComisionInmobiliaria.objects.create(
                ProyectoID=proyecto,
                PromesaFirmada=promesa_firmada,
                EscrituraFirmada=escritura_firmada,
                CierreGestion=cierre_gestion,
            )
        if proyecto:
            proyecto.IngresoComisionesState = IngresoComisionesState.objects.get(Name=constants.INGRESO_COMISIONES_STATE[1])
            current_user = return_current_user(self)
            project_director = self.create_notification(proyecto, notification_type=constants.NOTIFICATION_TYPE[47])
            log = self.create_project_log(proyecto, current_user)
            base_url = "http://" + get_current_site(self.context.get('request')).domain
            if project_director:
                file_url = base_url + settings.MEDIA_URL + log.ProyectoDetailDocument.name
                send_mail(message=file_url,
                          subject="Created a sale commission",
                          from_email=settings.EMAIL_HOST_USER,
                          recipient_list=[user.UserID.Email for user in project_director],
                          html_message="<a href='%s'>PDF FILE</a>" % file_url)
            proyecto.save()

        return comisiones

# Serializador para modificar comisiones a un proyecto


class UpdateComisionesSerializer(serializers.ModelSerializer):
    PromesaFirmada = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        required=False
    )
    EscrituraFirmada = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        required=False
    )
    CierreGestion = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        required=False
    )
    State = serializers.CharField(required=False)
    NoExisted = serializers.BooleanField(required=False)

    class Meta:
        model = ComisionInmobiliaria
        fields = ('PromesaFirmada', 'EscrituraFirmada',
                  'CierreGestion', 'State', 'NoExisted')

    def update(self, instance, validated_data):
        promesa_firmada = validated_data.get('PromesaFirmada', False)
        escritura_firmada = validated_data.get('EscrituraFirmada', False)
        cierre_gestion = validated_data.get('CierreGestion', False)
        state = validated_data.get('State', False)
        no_existed = validated_data.get('NoExisted', False)

        if promesa_firmada is not False:
            instance.PromesaFirmada = promesa_firmada
        if escritura_firmada is not False:
            instance.EscrituraFirmada = escritura_firmada
        if cierre_gestion is not False:
            instance.CierreGestion = cierre_gestion
        if state is not False:
            if state not in constants.DocumentState.values():
                raise ValidationError("State value is not valid!")
            instance.State = state
        else:
            instance.State = constants.DocumentState.TO_CONFIRM
        if no_existed is not False:
            instance.NoExisted = no_existed
        instance.save()
        CreateComisionesSerializer.create_notification(instance.ProyectoID,
                                                       notification_type=constants.NOTIFICATION_TYPE[48])

        return instance


class ComisionesSerializer(serializers.ModelSerializer):
    PromesaFirmada = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    EscrituraFirmada = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    CierreGestion = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    State = serializers.CharField(read_only=True)

    class Meta:
        model = ComisionInmobiliaria
        fields = ('PromesaFirmada', 'EscrituraFirmada',
                  'CierreGestion', 'State')


class FacturaInmuebleSerializer(serializers.ModelSerializer):
    InmuebleID = serializers.CharField(
        source="InmuebleID.InmuebleID"
    )
    InmuebleType = serializers.CharField(
        source="InmuebleID.InmuebleTypeID.Name"
    )
    Number = serializers.IntegerField(
        source="InmuebleID.Number"
    )
    Price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )

    class Meta:
        model = FacturaInmueble
        fields = ('InmuebleID', 'InmuebleType', 'Number', 'FolioVenta',
                  'Price', 'Comision', 'Tipo', 'State')


class RetrieveFacturaSerializer(serializers.ModelSerializer):
    InmobiliariaID = serializers.CharField(
        source='InmobiliariaID.InmobiliariaID'
    )
    Inmobiliaria = serializers.CharField(
        source='InmobiliariaID.RazonSocial'
    )
    Value = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True
    )
    Date = serializers.SerializerMethodField('get_date')
    DateEnvio = serializers.SerializerMethodField('get_date_envio')
    DatePayment = serializers.SerializerMethodField('get_date_payment')
    Inmuebles = serializers.SerializerMethodField('get_inmuebles')

    class Meta:
        model = Factura
        fields = ('FacturaID', 'InmobiliariaID', 'Inmobiliaria',
                  'Number', 'Date', 'DateEnvio',
                  'DatePayment', 'Value', 'Inmuebles')

    def get_date(self, obj):
        try:
            return obj.Date.strftime("%Y-%m-%d")
        except AttributeError:
            return ""

    def get_date_envio(self, obj):
        try:
            return obj.DateEnvio.strftime("%Y-%m-%d")
        except AttributeError:
            return ""

    def get_date_payment(self, obj):
        try:
            return obj.DatePayment.strftime("%Y-%m-%d")
        except AttributeError:
            return ""

    def get_inmuebles(self, obj):
        inmuebles_factura = FacturaInmueble.objects.filter(
            FacturaID=obj)
        serializer = ListCotizacionesInmueblesSerializer(
            instance=inmuebles_factura, many=True)
        return serializer.data


class ListFacturaSerializer(serializers.ModelSerializer):
    Date = serializers.SerializerMethodField('get_date')

    class Meta:
        model = Factura
        fields = ('FacturaID', 'Number', 'Date')

    def get_date(self, obj):
        try:
            return obj.Date.strftime("%Y-%m-%d")
        except AttributeError:
            return ""


def download_factura(instance, response):
    inmuebles_factura = FacturaInmueble.objects.filter(
        FacturaID=instance, State=constants.FACTURA_INMUEBLE_STATE[0])

    context_dict = {
        'factura': instance,
        'inmuebles': inmuebles_factura,
        'tamaño_letra': 100,
    }
    pdf = render_create_factura_to_pdf(context_dict, response)

    name = "FACTURA%s" % instance.Number
    return name


def download_nota_credito(instance, response):
    inmuebles_factura = FacturaInmueble.objects.filter(
        FacturaID=instance, State=constants.FACTURA_INMUEBLE_STATE[0])

    context_dict = {
        'factura': instance,
        'inmuebles': inmuebles_factura,
        'tamaño_letra': 100,
    }
    pdf = render_create_nota_credito_to_pdf(context_dict, response)

    name = "NOTA_CREDITO%s" % instance.Number
    return name


class RegisterSendFacturaSerializer(serializers.ModelSerializer):
    Number = serializers.IntegerField(
        write_only=True
    )
    DateEnvio = serializers.DateTimeField(
        write_only=True
    )
    FacturaState = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Factura
        fields = ('FacturaState', 'DateEnvio',
                  'Number')

    def update(self, instance, validated_data):
        date_envio = validated_data.get('DateEnvio')
        number = validated_data.get('Number')

        instance.DateEnvio = date_envio
        instance.Number = number
        instance.FacturaState = constants.FACTURA_STATE[0]

        instance.save()

        return instance


class RegisterDatePagoFacturaSerializer(serializers.ModelSerializer):
    DatePayment = serializers.DateTimeField(
        write_only=True
    )
    FacturaState = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Factura
        fields = ('FacturaState', 'DatePayment')

    def update(self, instance, validated_data):
        date_payment = validated_data.get('DatePayment')

        instance.DatePayment = date_payment
        instance.FacturaState = constants.FACTURA_STATE[1]

        instance.save()

        return instance
