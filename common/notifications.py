from django.shortcuts import get_object_or_404
from . import constants
from .models import Notification, NotificationType
from users.models import User
from common.services import formatear_rut


# Funciones para la creacion de notificaciones


def crear_notificacion_cambio_clave(user):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[8])
    message = "Debes cambiar tu contraseña inicial"

    notification = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=user.UserID,
        Message=message,
        RedirectRouteID=None
    )
    notification.UserID.add(user)


def crear_notificacion_inmobiliaria_sin_representante(
        inmobiliaria, current_user):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[0])
    notification = Notification.objects.filter(
        TableID=inmobiliaria.InmobiliariaID,
        NotificationTypeID=notification_type)

    rut_formateado = formatear_rut(inmobiliaria.Rut)
    message = "%s (%s) no tiene representante asignado y es una inmobiliaria" % (
        inmobiliaria.RazonSocial, rut_formateado)

    if not notification.exists():
        notification = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=inmobiliaria.InmobiliariaID,
            Message=message,
            RedirectRouteID=inmobiliaria.InmobiliariaID
        )
        notification.UserID.add(current_user)


def crear_notificacion_inmobiliaria_sin_aprobador(inmobiliaria, current_user):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[9])
    notification = Notification.objects.filter(
        TableID=inmobiliaria.InmobiliariaID,
        NotificationTypeID=notification_type)

    rut_formateado = formatear_rut(inmobiliaria.Rut)
    message = "%s (%s) no tiene aprobador asignado y es una inmobiliaria" % (
        inmobiliaria.RazonSocial, rut_formateado)

    if not notification.exists():
        notification = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=inmobiliaria.InmobiliariaID,
            Message=message,
            RedirectRouteID=inmobiliaria.InmobiliariaID
        )
        notification.UserID.add(current_user)


def crear_notificacion_aprobar_proyecto(
        proyecto,
        jefe_proyecto,
        area_approve):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[6])

    message = "Proyecto %s aprobado por %s" % (proyecto.Name, area_approve)

    notification = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=proyecto.ProyectoID,
        Message=message,
        RedirectRouteID=proyecto.ProyectoID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification.UserID.add(jefe.UserID)


def crear_notificacion_rechazar_proyecto(proyecto, jefe_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[7])

    message = "Proyecto %s rechazado" % (proyecto.Name)

    notification = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=proyecto.ProyectoID,
        Message=message,
        RedirectRouteID=proyecto.ProyectoID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification.UserID.add(jefe.UserID)


def crear_notificacion_proyecto_sin_jefe_proyecto(
        proyecto,
        creator,
        usuarios_monitorea_proyectos):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[4])

    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    message = "Proyecto %s no tiene jefe de proyecto" % (proyecto.Name)

    if not notification.exists():
        notification = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=proyecto.ProyectoID,
            Message=message,
            RedirectRouteID=proyecto.ProyectoID
        )
        notification.UserID.add(creator.UserID)

        for usuario_monitorea_proyectos in usuarios_monitorea_proyectos:
            notification.UserID.add(usuario_monitorea_proyectos)


def crear_notificacion_proyecto_sin_representantes(
        proyecto,
        creator,
        jefe_proyecto,
        usuarios_monitorea_proyectos):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[1])

    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    message = "%s (%s) no tiene representante asignado" % (
        proyecto.Name, proyecto.Symbol)

    if not notification.exists():
        notification = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=proyecto.ProyectoID,
            Message=message,
            RedirectRouteID=proyecto.ProyectoID
        )
        notification.UserID.add(creator.UserID)

        if jefe_proyecto.exists():
            for jefe in jefe_proyecto:
                notification.UserID.add(jefe.UserID)

        for usuario_monitorea_proyectos in usuarios_monitorea_proyectos:
            notification.UserID.add(usuario_monitorea_proyectos)


def crear_notificacion_proyecto_sin_vendedores(
        proyecto,
        creator,
        jefe_proyecto,
        usuarios_monitorea_proyectos):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[2])

    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    message = "%s (%s) no tiene vendedor asignado" % (
        proyecto.Name, proyecto.Symbol)

    if not notification.exists():
        notification = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=proyecto.ProyectoID,
            Message=message,
            RedirectRouteID=proyecto.ProyectoID
        )
        notification.UserID.add(creator.UserID)

        if jefe_proyecto.exists():
            for jefe in jefe_proyecto:
                notification.UserID.add(jefe.UserID)

        for usuario_monitorea_proyectos in usuarios_monitorea_proyectos:
            notification.UserID.add(usuario_monitorea_proyectos)


def crear_notificacion_proyecto_sin_asistentes_comerciales(
        proyecto,
        creator,
        jefe_proyecto,
        usuarios_monitorea_proyectos):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[3])

    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    message = "Proyecto %s no tiene asistente comercial" % (proyecto.Name)

    if not notification.exists():
        notification = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=proyecto.ProyectoID,
            Message=message,
            RedirectRouteID=proyecto.ProyectoID
        )
        notification.UserID.add(creator.UserID)

        if jefe_proyecto.exists():
            for jefe in jefe_proyecto:
                notification.UserID.add(jefe.UserID)

        for usuario_monitorea_proyectos in usuarios_monitorea_proyectos:
            notification.UserID.add(usuario_monitorea_proyectos)


def crear_notificacion_proyecto_sin_aprobador(
        proyecto,
        creator,
        jefe_proyecto,
        usuarios_monitorea_proyectos):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[10])

    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    message = "Proyecto %s no tiene aprobador" % (proyecto.Name)

    if not notification.exists():
        notification = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=proyecto.ProyectoID,
            Message=message,
            RedirectRouteID=proyecto.ProyectoID
        )
        notification.UserID.add(creator.UserID)

        if jefe_proyecto.exists():
            for jefe in jefe_proyecto:
                notification.UserID.add(jefe.UserID)

        for usuario_monitorea_proyectos in usuarios_monitorea_proyectos:
            notification.UserID.add(usuario_monitorea_proyectos)


def crear_notificacion_usuarios_aprueba_inmuebles(
        proyecto, usuarios_aprueba_inmuebles):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[5])

    message = "Proyecto %s, requiere aprobación" % (proyecto.Name)
    notification_created = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification_created:
        is_created = True
    else:
        is_created = False
        notification = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=proyecto.ProyectoID,
            Message=message,
            RedirectRouteID=proyecto.ProyectoID
        )

        for usuario_aprueba_inmuebles in usuarios_aprueba_inmuebles:
            notification.UserID.add(usuario_aprueba_inmuebles)

    return is_created


def crear_notificacion_usuarios_monitorea_proyectos(
        proyecto, usuarios_monitorea_proyectos):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[5])

    message = "Proyecto %s, requiere aprobación" % (proyecto.Name)
    notification_created = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification_created:
        is_created = True
    else:
        is_created = False
        notification = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=proyecto.ProyectoID,
            Message=message,
            RedirectRouteID=proyecto.ProyectoID
        )

        for usuario_monitorea_proyectos in usuarios_monitorea_proyectos:
            notification.UserID.add(usuario_monitorea_proyectos)

    return is_created


def crear_notificacion_etapa_sin_fecha_de_ventas(
        etapa,
        current_user,
        jefe_proyecto,
        usuarios_monitorea_proyectos):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[11])

    notification = Notification.objects.filter(
        TableID=etapa.EtapaID, NotificationTypeID=notification_type)

    message = "La etapa %s del proyecto %s no tiene fecha de ventas asignada" % (
        etapa.Name, etapa.ProyectoID.Name)

    if not notification.exists():
        notification_add = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=etapa.EtapaID,
            Message=message,
            RedirectRouteID=etapa.EtapaID
        )
        notification_add.UserID.add(current_user)

        if jefe_proyecto.exists():
            for jefe in jefe_proyecto:
                notification_add.UserID.add(jefe.UserID)

        for usuario_monitorea_proyectos in usuarios_monitorea_proyectos:
            notification_add.UserID.add(usuario_monitorea_proyectos)


def crear_notificacion_proyecto_sin_institucion_financiera(
        proyecto,
        current_user,
        jefe_proyecto,
        usuarios_monitorea_proyectos):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[12])

    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    message = "Proyecto %s no tiene institución financiera asignada" % (
        proyecto.Name)

    if not notification.exists():
        notification_add = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=proyecto.ProyectoID,
            Message=message,
            RedirectRouteID=proyecto.ProyectoID
        )
        notification_add.UserID.add(current_user)

        if jefe_proyecto.exists():
            for jefe in jefe_proyecto:
                notification_add.UserID.add(jefe.UserID)

        for usuario_monitorea_proyectos in usuarios_monitorea_proyectos:
            notification_add.UserID.add(usuario_monitorea_proyectos)


def crear_notificacion_proyecto_sin_aseguradora(
        proyecto,
        current_user,
        jefe_proyecto,
        usuarios_monitorea_proyectos):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[13])

    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    message = "Proyecto %s no tiene aseguradora asignada" % (proyecto.Name)

    if not notification.exists():
        notification_add = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=proyecto.ProyectoID,
            Message=message,
            RedirectRouteID=proyecto.ProyectoID
        )
        notification_add.UserID.add(current_user)

        if jefe_proyecto.exists():
            for jefe in jefe_proyecto:
                notification_add.UserID.add(jefe.UserID)

        for usuario_monitorea_proyectos in usuarios_monitorea_proyectos:
            notification_add.UserID.add(usuario_monitorea_proyectos)


def crear_notificacion_proyecto_pendiente_aprobacion(
        proyecto,
        jefe_proyecto,
        area_approve):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[14])
    message = "Proyecto %s, pendiente a aprobación %s" % (
        proyecto.Name, area_approve)

    notification = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=proyecto.ProyectoID,
        Message=message,
        RedirectRouteID=proyecto.ProyectoID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification.UserID.add(jefe.UserID)


def crear_notificacion_proyecto_sin_constructora(
        proyecto,
        current_user,
        jefe_proyecto,
        usuarios_monitorea_proyectos):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[15])

    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    message = "Proyecto %s no tiene constructora asignada" % (proyecto.Name)

    if not notification.exists():
        notification_add = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=proyecto.ProyectoID,
            Message=message,
            RedirectRouteID=proyecto.ProyectoID
        )
        notification_add.UserID.add(current_user)

        if jefe_proyecto.exists():
            for jefe in jefe_proyecto:
                notification_add.UserID.add(jefe.UserID)

        for usuario_monitorea_proyectos in usuarios_monitorea_proyectos:
            notification_add.UserID.add(usuario_monitorea_proyectos)


def crear_notificacion_proyecto_sin_inmuebles(
        proyecto,
        current_user,
        jefe_proyecto,
        usuarios_monitorea_proyectos):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[16])

    message = "Proyecto %s no tiene inmuebles" % (proyecto.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=proyecto.ProyectoID,
        Message=message,
        RedirectRouteID=proyecto.ProyectoID
    )
    notification_add.UserID.add(current_user)

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    for usuario_monitorea_proyectos in usuarios_monitorea_proyectos:
        notification_add.UserID.add(usuario_monitorea_proyectos)


def crear_notificacion_reserva_pendiente_informacion(
        reserva,
        jefe_proyecto,
        current_user):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[17])

    message = "Reserva %s proyecto %s, tiene información pendiente" % (
        reserva.Folio, reserva.ProyectoID.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=reserva.ReservaID,
        Message=message,
        RedirectRouteID=reserva.ReservaID
    )
    notification_add.UserID.add(current_user)

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)


def crear_notificacion_reserva_pendiente_control(
        reserva,
        jefe_proyecto,
        asistente_comercial):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[18])

    message = "Reserva %s proyecto %s, en espera de control" % (
        reserva.Folio, reserva.ProyectoID.Name)
    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=reserva.ReservaID,
        Message=message,
        RedirectRouteID=reserva.ReservaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if asistente_comercial.exists():
        for asistente in asistente_comercial:
            notification_add.UserID.add(asistente.UserID)


def crear_notificacion_reserva_rechazada(
        reserva,
        jefe_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[19])

    message = "Reserva %s proyecto %s rechazada" % (
        reserva.Folio, reserva.ProyectoID.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=reserva.ReservaID,
        Message=message,
        RedirectRouteID=reserva.ReservaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)


def crear_notificacion_reserva_cancelada(
        reserva,
        jefe_proyecto,
        vendedor_proyecto,
        asistente_comercial):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[19])

    message = "Reserva %s proyecto %s cancelada" % (
        reserva.Folio, reserva.ProyectoID.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=reserva.ReservaID,
        Message=message,
        RedirectRouteID=reserva.ReservaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)

    if asistente_comercial.exists():
        for asistente in asistente_comercial:
            notification_add.UserID.add(asistente.UserID)


def crear_notificacion_reserva_modificada_pendiente_informacion(
        reserva,
        jefe_proyecto,
        vendedor_proyecto,
        asistente_comercial):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[20])

    message = "Reserva %s proyecto %s modificada, con información pendiente" % (
         reserva.Folio, reserva.ProyectoID.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=reserva.ReservaID,
        Message=message,
        RedirectRouteID=reserva.ReservaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)

    if asistente_comercial.exists():
        for asistente in asistente_comercial:
            notification_add.UserID.add(asistente.UserID)


def crear_notificacion_reserva_modificada_pendiente_control(
        reserva,
        jefe_proyecto,
        vendedor_proyecto,
        asistente_comercial):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[21])

    message = "Reserva %s proyecto %s modificada, en espera de control" % (
        reserva.Folio, reserva.ProyectoID.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=reserva.ReservaID,
        Message=message,
        RedirectRouteID=reserva.ReservaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)

    if asistente_comercial.exists():
        for asistente in asistente_comercial:
            notification_add.UserID.add(asistente.UserID)


def crear_notificacion_proyecto_sin_borrador_promesa(proyecto, usuarios_aprueba_inmuebles):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[23])

    message = "Proyecto %s, falta agregar borrador de promesa" % (proyecto.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=proyecto.ProyectoID,
        Message=message,
        RedirectRouteID=proyecto.ProyectoID
    )

    for usuario_aprueba_inmuebles in usuarios_aprueba_inmuebles:
        notification_add.UserID.add(usuario_aprueba_inmuebles)


def crear_notificacion_oferta_creada(
        oferta,
        proyecto,
        jefe_proyecto,
        vendedor_proyecto,
        asistente_comercial,
        usuarios_recepciona_garantias):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[36])

    message = "Oferta %s proyecto %s ha sido creada" % (
        oferta.Folio, proyecto.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=oferta.OfertaID,
        Message=message,
        RedirectRouteID=oferta.OfertaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)

    if asistente_comercial.exists():
        for asistente in asistente_comercial:
            notification_add.UserID.add(asistente.UserID)

    for usuario_recepciona_garantias in usuarios_recepciona_garantias:
        notification_add.UserID.add(usuario_recepciona_garantias)


def crear_notificacion_oferta_pendiente_aprobacion_inmobiliaria(
        oferta,
        representante_proyecto,
        aprobador_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[25])

    message = "Oferta %s proyecto %s requiere aprobación" % (oferta.Folio, oferta.ProyectoID)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=oferta.OfertaID,
        Message=message,
        RedirectRouteID=oferta.OfertaID
    )

    for representante in representante_proyecto:
        notification_add.UserID.add(representante.UserID)

    for aprobador in aprobador_proyecto:
        notification_add.UserID.add(aprobador.UserID)

def crear_notificacion_modify_oferta_aprobada(
        oferta,
        jefe_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[50])

    message = "Oferta %s proyecto %s aprobada" % (
        oferta.Folio, oferta.ProyectoID)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=oferta.OfertaID,
        Message=message,
        RedirectRouteID=oferta.OfertaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)
       
def crear_notificacion_modify_oferta_rechazada(
        oferta,
        jefe_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[49])

    message = "Oferta %s proyecto %s rechazada" % (
        oferta.Folio, oferta.ProyectoID)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=oferta.OfertaID,
        Message=message,
        RedirectRouteID=oferta.OfertaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)       
       
def crear_notificacion_oferta_aprobada(
        oferta,
        jefe_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[26])

    message = "Oferta %s proyecto %s aprobada" % (
        oferta.Folio, oferta.ProyectoID)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=oferta.OfertaID,
        Message=message,
        RedirectRouteID=oferta.OfertaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)


def crear_notificacion_oferta_rechazada(
        oferta,
        jefe_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[27])

    message = "Oferta %s proyecto %s rechazada" % (
        oferta.Folio, oferta.ProyectoID)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=oferta.OfertaID,
        Message=message,
        RedirectRouteID=oferta.OfertaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)


def crear_notificacion_pre_aprobacion_aprobada(
        oferta,
        jefe_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[28])

    message = "Preaprobacion del credito para la oferta %s proyecto %s ha sido aprobada" % (
        oferta.Folio, oferta.ProyectoID)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=oferta.OfertaID,
        Message=message,
        RedirectRouteID=oferta.OfertaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)


def crear_notificacion_pre_aprobacion_rechazada(
        oferta,
        jefe_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[29])

    message = "Preaprobacion del credito para la oferta %s proyecto %s ha sido rechazada" % (
        oferta.Folio, oferta.ProyectoID)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=oferta.OfertaID,
        Message=message,
        RedirectRouteID=oferta.OfertaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)


def crear_notificacion_oferta_a_confeccion_promesa(
        oferta,
        jefe_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[30])

    message = "Oferta %s proyecto %s pendiente aprobación confección de promesa" % (
        oferta.Folio, oferta.ProyectoID.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=oferta.OfertaID,
        Message=message,
        RedirectRouteID=oferta.OfertaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)

def crear_notificacion_oferta_refund(oferta,
        jefe_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[53])

    message = "Oferta %s proyecto %s refund" % (
        oferta.Folio, oferta.ProyectoID.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=oferta.OfertaID,
        Message=message,
        RedirectRouteID=oferta.OfertaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)

def crear_notificacion_oferta_requiere_aprobacion(
        oferta,
        usuarios_aprueba_confeccion_promesa):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
        notification_type = NotificationType.objects.get(
            Name=constants.NOTIFICATION_TYPE[31])

        message = "Oferta %s proyecto %s requiere aprobación confección de promesa" % (
            oferta.Folio, oferta.ProyectoID.Name)

        notification_add = Notification.objects.create(
            NotificationTypeID=notification_type,
            TableID=oferta.OfertaID,
            Message=message,
            RedirectRouteID=oferta.OfertaID
        )
        for usuario_aprueba_confeccion_promesa in usuarios_aprueba_confeccion_promesa:
            notification_add.UserID.add(usuario_aprueba_confeccion_promesa)


def crear_notificacion_confeccion_promesa_aprobada(
        oferta,
        jefe_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[32])

    message = "Confeccion promesa para oferta %s proyecto %s ha sido aprobada" % (
        oferta.Folio, oferta.ProyectoID.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=oferta.OfertaID,
        Message=message,
        RedirectRouteID=oferta.OfertaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)


def crear_notificacion_confeccion_promesa_rechazada(
        oferta,
        jefe_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[33])

    message = "Confeccion promesa para oferta %s proyecto %s ha sido rechazada" % (
        oferta.Folio, oferta.ProyectoID.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=oferta.OfertaID,
        Message=message,
        RedirectRouteID=oferta.OfertaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)


def crear_notificacion_oferta_cancelada(
        oferta,
        jefe_proyecto,
        vendedor_proyecto,
        asistente_comercial,
        representante_proyecto,
        aprobador_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[34])

    message = "Oferta %s proyecto %s cancelada" % (
        oferta.Folio, oferta.ProyectoID.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=oferta.OfertaID,
        Message=message,
        RedirectRouteID=oferta.OfertaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)

    if asistente_comercial.exists():
        for asistente in asistente_comercial:
            notification_add.UserID.add(asistente.UserID)

    if representante_proyecto:
        for representante in representante_proyecto:
            notification_add.UserID.add(representante.UserID)

    if aprobador_proyecto:
        for aprobador in aprobador_proyecto:
            notification_add.UserID.add(aprobador.UserID)


def crear_notificacion_oferta_modificada(
        oferta,
        jefe_proyecto,
        vendedor_proyecto,
        asistente_comercial):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[35])

    message = "Oferta %s proyecto %s modificada" % (
         oferta.Folio, oferta.ProyectoID.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=oferta.OfertaID,
        Message=message,
        RedirectRouteID=oferta.OfertaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)

    if asistente_comercial.exists():
        for asistente in asistente_comercial:
            notification_add.UserID.add(asistente.UserID)


def crear_notificacion_promesa_creada(
        promesa,
        proyecto,
        jefe_proyecto,
        vendedor_proyecto,
        usuarios_confecciona_maquetas):

    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[36])

    message = "Promesa %s proyecto %s ha sido creada" % (
        promesa.Folio, proyecto.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=promesa.PromesaID,
        Message=message,
        RedirectRouteID=promesa.PromesaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)

    for usuario_confecciona_maquetas in usuarios_confecciona_maquetas:
        notification_add.UserID.add(usuario_confecciona_maquetas)


def crear_notificacion_maqueta_aprobada(promesa, vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[37])

    message = "Confeccion maqueta promesa %s proyecto %s ha sido aprobada" % (
        promesa.Folio, promesa.ProyectoID.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=promesa.PromesaID,
        Message=message,
        RedirectRouteID=promesa.PromesaID
    )

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)


def crear_notificacion_maqueta_rechazada(promesa, usuarios_confecciona_maquetas):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[38])

    message = "Confeccion maqueta promesa %s proyecto %s ha sido rechazada" % (
        promesa.Folio, promesa.ProyectoID.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=promesa.PromesaID,
        Message=message,
        RedirectRouteID=promesa.PromesaID
    )

    for usuario_confecciona_maquetas in usuarios_confecciona_maquetas:
        notification_add.UserID.add(usuario_confecciona_maquetas)


def crear_notificacion_promesa_aprobada(
        promesa,
        proyecto,
        jefe_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[39])

    message = "Promesa %s proyecto %s ha sido aprobada" % (
        promesa.Folio, proyecto.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=promesa.PromesaID,
        Message=message,
        RedirectRouteID=promesa.PromesaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)


def crear_notificacion_promesa_rechazada(
        promesa,
        proyecto,
        jefe_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[40])

    message = "Promesa %s proyecto %s ha sido rechazada" % (
        promesa.Folio, proyecto.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=promesa.PromesaID,
        Message=message,
        RedirectRouteID=promesa.PromesaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)


def crear_notificacion_promesa_enviada_a_inmobiliaria(
        promesa,
        proyecto,
        representante_proyecto,
        aprobador_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[41])

    message = "Promesa %s proyecto %s ha sido enviada a inmobiliaria" % (
        promesa.Folio, proyecto.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=promesa.PromesaID,
        Message=message,
        RedirectRouteID=promesa.PromesaID
    )

    if representante_proyecto:
        for representante in representante_proyecto:
            notification_add.UserID.add(representante.UserID)

    if aprobador_proyecto:
        for aprobador in aprobador_proyecto:
            notification_add.UserID.add(aprobador.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)


def crear_notificacion_copias_enviadas(
        promesa,
        proyecto,
        representante_proyecto,
        aprobador_proyecto,
        jefe_proyecto,
        vendedor_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[42])

    message = "Promesa %s proyecto %s copias han sido enviadas" % (
        promesa.Folio, proyecto.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=promesa.PromesaID,
        Message=message,
        RedirectRouteID=promesa.PromesaID
    )

    if representante_proyecto:
        for representante in representante_proyecto:
            notification_add.UserID.add(representante.UserID)

    if aprobador_proyecto:
        for aprobador in aprobador_proyecto:
            notification_add.UserID.add(aprobador.UserID)

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)

    if vendedor_proyecto.exists():
        for vendedor in vendedor_proyecto:
            notification_add.UserID.add(vendedor.UserID)


def crear_notificacion_promesa_modificada(
        promesa,
        proyecto,
        jefe_proyecto):
    # Tipo de notificacion a crear en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[43])

    message = "Promesa %s proyecto %s ha sido modificada, revise modificaciones" % (
        promesa.Folio, proyecto.Name)

    notification_add = Notification.objects.create(
        NotificationTypeID=notification_type,
        TableID=promesa.PromesaID,
        Message=message,
        RedirectRouteID=promesa.PromesaID
    )

    if jefe_proyecto.exists():
        for jefe in jefe_proyecto:
            notification_add.UserID.add(jefe.UserID)


def eliminar_notificacion_cambio_clave(current_user):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[8])
    user = get_object_or_404(User, Rut=current_user)
    notification = Notification.objects.filter(
        UserID=user, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_inmobiliaria_sin_representante(inmobiliaria):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[0])
    notification = Notification.objects.filter(
        TableID=inmobiliaria.InmobiliariaID,
        NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_inmobiliaria_sin_aprobador(inmobiliaria):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[9])
    notification = Notification.objects.filter(
        TableID=inmobiliaria.InmobiliariaID,
        NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_proyecto_aprobado(proyecto, current_user):
    user = get_object_or_404(User, Rut=current_user)
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[6])
    notifications = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    # Se elimina al usuario actual de la notificacion
    for notification in notifications:
            notification.UserID.remove(user)

    # Si no hay mas usuarios, se elimina la notificacion 
    for notification in notifications:
        if not notification.UserID.all():
            notification.delete()

def eliminar_notificacion_proyecto_aprobacion(proyecto):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[5])
    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_proyecto_sin_representante(proyecto):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[1])
    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_proyecto_sin_jefe_proyecto(proyecto):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[4])
    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_proyecto_sin_vendedores(proyecto):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[2])
    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_proyecto_sin_asistentes_comerciales(proyecto):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[3])
    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_proyecto_sin_aprobador(proyecto):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[10])
    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_proyecto_rechazado(proyecto, current_user):
    user = get_object_or_404(User, Rut=current_user)
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[7])
    notifications = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    # Se elimina al usuario actual de la notificacion
    for notification in notifications:
            notification.UserID.remove(user)

    # Si no hay mas usuarios, se elimina la notificacion 
    for notification in notifications:
        if not notification.UserID.all():
            notification.delete()


def eliminar_notificacion_etapa_sin_fecha_de_ventas(proyecto):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[11])
    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_proyecto_sin_institucion_financiera(proyecto):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[12])
    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_proyecto_sin_aseguradora(proyecto):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[13])
    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_proyecto_pendiente_aprobacion(proyecto):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[14])
    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_proyecto_sin_constructora(proyecto):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[15])
    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_proyecto_sin_inmuebles(proyecto):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[16])
    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_reserva_informacion_pendiente(reserva):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[17])
    notification = Notification.objects.filter(
        TableID=reserva.ReservaID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_reserva_pendiente_control(reserva):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[18])
    notification = Notification.objects.filter(
        TableID=reserva.ReservaID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_reserva_rechazada(reserva, current_user):
    user = get_object_or_404(User, Rut=current_user)
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[19])
    notifications = Notification.objects.filter(
        TableID=reserva.ReservaID, NotificationTypeID=notification_type)

    # Se elimina al usuario actual de la notificacion
    for notification in notifications:
            notification.UserID.remove(user)

    # Si no hay mas usuarios, se elimina la notificacion 
    for notification in notifications:
        if not notification.UserID.all():
            notification.delete()


def eliminar_notificacion_reserva_cancelada(reserva, current_user):
    user = get_object_or_404(User, Rut=current_user)
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[20])
    notifications = Notification.objects.filter(
        TableID=reserva.ReservaID, NotificationTypeID=notification_type)

    # Se elimina al usuario actual de la notificacion
    for notification in notifications:
            notification.UserID.remove(user)

    # Si no hay mas usuarios, se elimina la notificacion 
    for notification in notifications:
        if not notification.UserID.all():
            notification.delete()


def eliminar_notificacion_reserva_modificada_pendiente_informacion(reserva):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[20])
    notification = Notification.objects.filter(
        TableID=reserva.ReservaID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_reserva_modificada_pendiente_control(reserva):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[21])
    notification = Notification.objects.filter(
        TableID=reserva.ReservaID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificaciones_reserva(reserva):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification = Notification.objects.filter(
        TableID=reserva.ReservaID)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_borrador_promesa(proyecto):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[23])
    notification = Notification.objects.filter(
        TableID=proyecto.ProyectoID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_oferta_a_confeccion_promesa(oferta):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[30])
    notification = Notification.objects.filter(
        TableID=oferta.OfertaID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_oferta_requiere_aprobacion(oferta):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[31])
    notification = Notification.objects.filter(
        TableID=oferta.OfertaID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_confeccion_promesa_aprobada(oferta):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[32])
    notification = Notification.objects.filter(
        TableID=oferta.OfertaID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificacion_confeccion_promesa_rechazada(oferta):
    # Tipo de notificacion a eliminar en constants.py se encuentra los nombres de estas notificaciones
    notification_type = NotificationType.objects.get(
        Name=constants.NOTIFICATION_TYPE[33])
    notification = Notification.objects.filter(
        TableID=oferta.OfertaID, NotificationTypeID=notification_type)

    if notification.exists():
        notification.delete()


def eliminar_notificaciones_oferta(oferta):
    notification = Notification.objects.filter(
        TableID=oferta.OfertaID)

    if notification.exists():
        notification.delete()
