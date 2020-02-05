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
    crear_notificacion_desistimiento_aprobada
from common.services import return_current_user
from common.validations import CustomValidation
from empresas_and_proyectos.models.inmuebles import InmuebleState
from empresas_and_proyectos.models.proyectos import UserProyectoType, UserProyecto, Proyecto
from users.models import User, Permission, Role
from ventas.models.promesas import Promesa, PromesaInmueble
from ventas.models.ventas_logs import VentaLog, VentaLogType


def vnRegisterDesistimiento(promesa, validated_data):
    new_promesa_state = validated_data.pop('PromesaState')
    promesa.PromesaState = new_promesa_state
    if new_promesa_state == constants.PROMESA_STATE[16]:
        # V->JP
        promesa.PromesaDesistimientoState = constants.PROMESA_DESISTIMIENTO_STATE[0]
    if new_promesa_state == constants.PROMESA_STATE[17]:
        promesa.PromesaResiliacionState = constants.PROMESA_RESILIACION_STATE[0]
    if new_promesa_state == constants.PROMESA_STATE[18]:
        promesa.PromesaResolucionState = constants.PROMESA_RESLUCION_STATE[0]

    jefe_proyecto = UserProyecto.objects.filter(
        ProyectoID=promesa.ProyectoID,
        UserProyectoTypeID=UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1]))

    crear_notificacion_register_desistimiento_aprobada(promesa, jefe_proyecto)

    venta_log_type = VentaLogType.objects.get(
        Name=constants.VENTA_LOG_TYPE[36])

    return promesa, venta_log_type


def jpRegisterDesistimiento(promesa, validated_data):
    new_promesa_state = validated_data.pop('PromesaState')
    promesa.PromesaState = new_promesa_state

    venta_log_type = VentaLogType.objects.get(
        Name=constants.VENTA_LOG_TYPE[36])
    # Desistimiento
    if new_promesa_state == constants.PROMESA_STATE[16]:
        # JP -> FI
        promesa, venta_log_type = desistimiento(promesa)
    # Resiliacion
    if new_promesa_state == constants.PROMESA_STATE[17]:
        promesa.PromesaResiliacionState = constants.PROMESA_RESILIACION_STATE[1]
    # Resolucion
    if new_promesa_state == constants.PROMESA_STATE[18]:
        promesa.PromesaResolucionState = constants.PROMESA_RESLUCION_STATE[1]

    gc_users = User.objects.filter(RoleID=Role.objects.get(Name=constants.UserRole.GERENTE_COMERCIAL))
    crear_notificacion_register_desistimiento_aprobada(promesa, gc_users)

    return promesa, venta_log_type


def desistimiento(promesa):
    promesa.PromesaDesistimientoState = constants.PROMESA_DESISTIMIENTO_STATE[1]
    # release properties
    inmuebles = PromesaInmueble.objects.filter(PromesaID=promesa)
    if inmuebles.exists():
        for inmueble in inmuebles:
            inmueble_state = InmuebleState.objects.get(
                Name=constants.INMUEBLE_STATE[0]
            )
            inmueble.InmuebleID.InmuebleStateID = inmueble_state
            inmueble.InmuebleID.save()
        inmuebles.delete()
    # notify IN & FI
    representante_proyecto_type = UserProyectoType.objects.get(
        Name=constants.USER_PROYECTO_TYPE[0])
    aprobador_proyecto_type = UserProyectoType.objects.get(
        Name=constants.USER_PROYECTO_TYPE[4])
    representante_proyecto = UserProyecto.objects.filter(
        ProyectoID=instance.ProyectoID,
        UserProyectoTypeID=representante_proyecto_type)
    aprobador_proyecto = UserProyecto.objects.filter(
        ProyectoID=instance.ProyectoID,
        UserProyectoTypeID=aprobador_proyecto_type)
    crear_notificacion_desistimiento_aprobada(promesa, representante_proyecto, aprobador_proyecto)

    venta_log_type = VentaLogType.objects.get(
        Name=constants.VENTA_LOG_TYPE[37])

    return promesa, venta_log_type


# use for all kind of Desistimientos
# Todo: need update to handle Desistimientos > Modificación case
class RegisterDesistimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promesa
        fields = ('PromesaState', 'PromesaDesistimientoState', 'PromesaResiliacionState', 'PromesaResolucionState',
                  'PromesaModificacionState')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        desistimiento(instance)

        user = UserProyecto.objects.get(
            ProyectoID=instance.ProyectoID,
            UserID=current_user
        )

        vendedor_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[2])
        jefe_proyecto_type = UserProyectoType.objects.get(
            Name=constants.USER_PROYECTO_TYPE[1])

        if user.UserProyectoTypeID == vendedor_type.UserProyectoTypeID:
            instance, venta_log_type = vnRegisterDesistimiento(instance, validated_data)
        elif user.UserProyectoTypeID == jefe_proyecto_type.UserProyectoTypeID:
            instance, venta_log_type = jpRegisterDesistimiento(instance, validated_data)
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


class ApproveDesistimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promesa
        fields = ('PromesaState', 'PromesaDesistimientoState', 'PromesaResiliacionState', 'PromesaResolucionState',
                  'PromesaModificacionState')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        if instance.PromesaDesistimientoState == constants.PROMESA_DESISTIMIENTO_STATE[1]:
            raise CustomValidation(
                "Desistimiento ha aprobado",
                status_code=status.HTTP_409_CONFLICT)

        instance, venta_log_type = desistimiento(instance)

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
