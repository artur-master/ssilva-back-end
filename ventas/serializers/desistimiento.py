from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers, status

from common import constants
from common.notifications import crear_notificacion_promesa_creada, crear_notificacion_maqueta_jp_aprobada, \
    crear_notificacion_maqueta_aprobada, \
    crear_notificacion_maqueta_rechazada, crear_notificacion_promesa_aprobada, crear_notificacion_promesa_rechazada, \
    crear_notificacion_promesa_enviada_a_inmobiliaria, crear_notificacion_copias_enviadas, \
    crear_notificacion_promesa_modificada, \
    crear_notificacion_promesa_envio_a_negociacion, \
    crear_notificacion_promesa_control_negociacion, \
    crear_notificacion_promesa_aprobada_negociacion, \
    crear_notificacion_promesa_rechazada_negociacion, \
    crear_notificacion_register_desistimiento_aprobada, \
    crear_notificacion_release_properties
from common.services import return_current_user
from common.validations import CustomValidation
from empresas_and_proyectos.models.inmuebles import InmuebleState
from empresas_and_proyectos.models.proyectos import UserProyectoType, UserProyecto, Proyecto
from users.models import User, Permission, Role
from ventas.models.promesas import Promesa, PromesaInmueble
from ventas.models.ventas_logs import VentaLog, VentaLogType

'''
Step 1: Register Desistimiento (for all cases) - VN / JP
Step 2: Approve - GC / IN
'''


def vnRegisterDesistimiento(promesa, validated_data):
    new_promesa_state = validated_data.pop('PromesaState')
    promesa.PromesaState = new_promesa_state
    if new_promesa_state == constants.PROMESA_STATE[16]:
        # V->JP
        promesa.PromesaDesistimientoState = constants.PROMESA_DESISTIMIENTO_STATE[0]
    if new_promesa_state == constants.PROMESA_STATE[17]:
        promesa.PromesaResciliacionState = constants.PROMESA_RESCILIACION_STATE[0]
    if new_promesa_state == constants.PROMESA_STATE[18]:
        promesa.PromesaResolucionState = constants.PROMESA_RESOLUCION_STATE[0]

    jefe_proyecto = UserProyecto.objects.filter(
        ProyectoID=promesa.ProyectoID,
        UserProyectoTypeID=UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1]))

    crear_notificacion_register_desistimiento_aprobada(promesa, jefe_proyecto)

    venta_log_type = VentaLogType.objects.get(
        Name=constants.VENTA_LOG_TYPE[37])
    return promesa, venta_log_type


def jpRegisterDesistimiento(promesa, validated_data):
    new_promesa_state = validated_data.pop('PromesaState')
    promesa.PromesaState = new_promesa_state

    venta_log_type = VentaLogType.objects.get(
        Name=constants.VENTA_LOG_TYPE[37])
    # Desistimiento
    if new_promesa_state == constants.PROMESA_STATE[16]:
        if (promesa.PromesaDesistimientoState and
                promesa.PromesaDesistimientoState != constants.PROMESA_DESISTIMIENTO_STATE[0]):
            raise CustomValidation("Desistimiento es aprobado por JP", status_code=status.HTTP_409_CONFLICT)
        promesa.PromesaDesistimientoState = constants.PROMESA_REFUND_STATE[0]
        promesa, venta_log_type = releaseProperties(promesa)
    # Resciliacion
    if new_promesa_state == constants.PROMESA_STATE[17]:
        if (promesa.PromesaResciliacionState and
                promesa.PromesaResciliacionState == constants.PROMESA_RESCILIACION_STATE[1]):
            raise CustomValidation("Resciliación es aprobado por JP", status_code=status.HTTP_409_CONFLICT)
        promesa.PromesaResciliacionState = constants.PROMESA_RESCILIACION_STATE[1]
    # Resolucion
    if new_promesa_state == constants.PROMESA_STATE[18]:
        if (promesa.PromesaResolucionState and
                promesa.PromesaResolucionState == constants.PROMESA_RESOLUCION_STATE[1]):
            raise CustomValidation("Resolución es aprobado por JP", status_code=status.HTTP_409_CONFLICT)
        promesa.PromesaResolucionState = constants.PROMESA_RESOLUCION_STATE[1]

    gc_users = User.objects.filter(RoleID=Role.objects.get(Name=constants.UserRole.GERENTE_COMERCIAL).RoleID)
    crear_notificacion_register_desistimiento_aprobada(promesa, gc_users)
    return promesa, venta_log_type


def gcRegisterDesistimiento(promesa):
    venta_log_type = VentaLogType.objects.get(
        Name=constants.VENTA_LOG_TYPE[37])
    # Resciliacion
    if promesa.PromesaState == constants.PROMESA_STATE[17]:
        if (promesa.PromesaResciliacionState and
                promesa.PromesaResciliacionState == constants.PROMESA_RESCILIACION_STATE[2]):
            raise CustomValidation("Resciliación es aprobado por GC", status_code=status.HTTP_409_CONFLICT)
        promesa.PromesaResciliacionState = constants.PROMESA_RESCILIACION_STATE[2]
    # Resolucion
    if promesa.PromesaState == constants.PROMESA_STATE[18]:
        if (promesa.PromesaResolucionState and
                promesa.PromesaResolucionState == constants.PROMESA_RESOLUCION_STATE[2]):
            raise CustomValidation("Resolución es aprobado por GC", status_code=status.HTTP_409_CONFLICT)
        promesa.PromesaResolucionState = constants.PROMESA_RESOLUCION_STATE[2]

    representante_users = UserProyecto.objects.filter(
        ProyectoID=promesa.ProyectoID,
        UserProyectoTypeID=UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[0]))

    aprobador_users = UserProyecto.objects.filter(
        ProyectoID=promesa.ProyectoID,
        UserProyectoTypeID=UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[4]))

    crear_notificacion_register_desistimiento_aprobada(promesa, representante_users | aprobador_users)
    return promesa, venta_log_type


def inRegisterDesistimiento(promesa):
    venta_log_type = VentaLogType.objects.get(
        Name=constants.VENTA_LOG_TYPE[37])
    # Resciliacion
    if promesa.PromesaState == constants.PROMESA_STATE[17]:
        if (promesa.PromesaResciliacionState and
                promesa.PromesaResciliacionState == constants.PROMESA_RESCILIACION_STATE[3]):
            raise CustomValidation("Resciliación es aprobado por GC", status_code=status.HTTP_409_CONFLICT)
        promesa.PromesaResciliacionState = constants.PROMESA_RESCILIACION_STATE[3]
    # Resolucion
    if promesa.PromesaState == constants.PROMESA_STATE[18]:
        if (promesa.PromesaResolucionState and
                promesa.PromesaResolucionState == constants.PROMESA_RESOLUCION_STATE[3]):
            raise CustomValidation("Resolución es aprobado por GC", status_code=status.HTTP_409_CONFLICT)
        promesa.PromesaResolucionState = constants.PROMESA_RESOLUCION_STATE[3]

    return promesa, venta_log_type


# use for all kind of Desistimientos
# Todo: need update to handle Desistimientos > Modificación case
class RegisterDesistimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promesa
        fields = ('PromesaState', 'PromesaDesistimientoState', 'PromesaResciliacionState', 'PromesaResolucionState',
                  'PromesaModificacionState')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        if current_user.RoleID.filter(Name=constants.UserRole.GERENTE_COMERCIAL).count() > 0:
            instance, venta_log_type = gcRegisterDesistimiento(instance)
        else:
            count_users = UserProyecto.objects.filter(
                ProyectoID=instance.ProyectoID,
                UserID=current_user
            ).count()
            if count_users > 0 and current_user.RoleID.filter(Name=constants.UserRole.VENDEDOR).count() > 0:
                instance, venta_log_type = vnRegisterDesistimiento(instance, validated_data)
            elif count_users > 0 and current_user.RoleID.filter(Name=constants.UserRole.JEFE_DE_PROYECTO).count() > 0:
                instance, venta_log_type = jpRegisterDesistimiento(instance, validated_data)
            elif count_users > 0 and current_user.RoleID.filter(Name=constants.UserRole.INMOBILIARIO).count() > 0:
                instance, venta_log_type = inRegisterDesistimiento(instance)
            else:
                return instance

        VentaLog.objects.create(
            VentaID=instance.PromesaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=validated_data.get('Comment', '')
        )

        instance.save()

        return instance


'''
Step 3: Confección - JP / Client
'''


class UploadConfeccionDesistimientoSerializer(serializers.ModelSerializer):
    DocumentResciliacion = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentResciliacionFirma = serializers.FileField(
        allow_empty_file=True,
        required=False
    )
    DocumentResolucion = serializers.FileField(
        allow_empty_file=True,
        required=False
    )

    class Meta:
        model = Promesa
        fields = ('DocumentResciliacion', 'DocumentResciliacionFirma', 'DocumentResolucion',
                  'PromesaState', 'PromesaResciliacionState', 'PromesaResolucionState')

    def update(self, instance, validated_data):
        if instance.PromesaState == constants.PROMESA_STATE[17]:
            if 'DocumentResciliacion' in validated_data:
                instance.DocumentResciliacion = validated_data['DocumentResciliacion']
                instance.PromesaResciliacionState = constants.PROMESA_RESCILIACION_STATE[4]
            if 'DocumentResciliacionFirma' in validated_data:
                instance.DocumentResciliacionFirma = validated_data['DocumentResciliacionFirma']
                instance.PromesaResciliacionState = constants.PROMESA_REFUND_STATE[0]

        if instance.PromesaState == constants.PROMESA_STATE[18]:
            if 'DocumentResolucion' in validated_data:
                instance.DocumentResolucion = validated_data['DocumentResolucion']
                instance.PromesaResolucionState = constants.PROMESA_REFUND_STATE[0]

        instance.save()
        return instance


def releaseProperties(promesa):
    # release properties
    inmuebles = PromesaInmueble.objects.filter(PromesaID=promesa)
    if inmuebles.exists():
        for inmueble in inmuebles:
            inmueble_state = InmuebleState.objects.get(
                Name=constants.INMUEBLE_STATE[0]
            )
            inmueble.InmuebleID.InmuebleStateID = inmueble_state
            inmueble.InmuebleID.save()
        # inmuebles.delete()
    # notify IN & FI
    fi_proyecto_type = UserProyectoType.objects.get(
        Name=constants.USER_PROYECTO_TYPE[7])
    representante_proyecto_type = UserProyectoType.objects.get(
        Name=constants.USER_PROYECTO_TYPE[0])
    aprobador_proyecto_type = UserProyectoType.objects.get(
        Name=constants.USER_PROYECTO_TYPE[4])

    fi_proyecto = UserProyecto.objects.filter(
        ProyectoID=promesa.ProyectoID,
        UserProyectoTypeID=fi_proyecto_type)
    representante_proyecto = UserProyecto.objects.filter(
        ProyectoID=promesa.ProyectoID,
        UserProyectoTypeID=representante_proyecto_type)
    aprobador_proyecto = UserProyecto.objects.filter(
        ProyectoID=promesa.ProyectoID,
        UserProyectoTypeID=aprobador_proyecto_type)
    crear_notificacion_release_properties(promesa, fi_proyecto | representante_proyecto | aprobador_proyecto)

    venta_log_type = VentaLogType.objects.get(
        Name=constants.VENTA_LOG_TYPE[38])

    return promesa, venta_log_type


'''
Step 4: Refund - FI
'''


class RgisterRefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promesa
        fields = ('PromesaState', 'PromesaDesistimientoState', 'PromesaResciliacionState', 'PromesaResolucionState',
                  'PromesaModificacionState')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)
        current_state = ''
        # Desistimiento
        if instance.PromesaState == constants.PROMESA_STATE[16]:
            # get current state
            current_state = instance.PromesaDesistimientoState
            # apply new state
            instance.PromesaDesistimientoState = constants.PROMESA_REFUND_STATE[1]
        # Resciliacion
        if instance.PromesaState == constants.PROMESA_STATE[17]:
            current_state = instance.PromesaResciliacionState
            instance.PromesaResciliacionState = constants.PROMESA_REFUND_STATE[1]
        # Resolucion
        if instance.PromesaState == constants.PROMESA_STATE[18]:
            current_state = instance.PromesaResolucionState
            instance.PromesaResolucionState = constants.PROMESA_REFUND_STATE[1]

        if current_state == '' or current_state == constants.PROMESA_REFUND_STATE[1]:
            raise CustomValidation("Promesa garantia refund",
                                   status_code=status.HTTP_409_CONFLICT)

        venta_log_type = VentaLogType.objects.get(Name=constants.VENTA_LOG_TYPE[31])
        comment = "Promesa {0} garantia refund".format(instance.Folio)

        VentaLog.objects.create(
            VentaID=instance.PromesaID,
            Folio=instance.Folio,
            UserID=current_user,
            ClienteID=instance.ClienteID,
            ProyectoID=instance.ProyectoID,
            VentaLogTypeID=venta_log_type,
            Comment=comment
        )

        instance.save()

        return instance
