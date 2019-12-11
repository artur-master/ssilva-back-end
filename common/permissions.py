from users.models import User
from . import constants
from users import models
from empresas_and_proyectos.models.proyectos import (
    Proyecto,
    ProyectoApprovalState, UserProyecto)
from .services import return_permissions
from rest_framework import permissions


# Creacion de clases y funciones para la verificacion de permisos para restringir acceso a endpoints 

class IsOwnerUserProfile(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_object_permission(self, request, view, obj):
        has_permission = False
        permissions = return_permissions(request.user)
        user_profile = models.User.objects.get(Rut=request.user)

        # Verifica si el usuario actual puede ver su propio perfil
        if obj.id == user_profile.id:
            has_permission = True

        # Verifica si el usuario actual tiene los permisos Administra usuarios o Consulta usuarios para ver el perfil de otro usuario
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[1]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[5]:
                has_permission = True

        return has_permission


class CheckAdminOrConsRolePermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)
        has_permission = False
        
        # Verifica si el usuario actual tiene los permisos Administra roles o Consulta roles 
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[4]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[0]:
                has_permission = True
        return has_permission


class CheckAdminRolePermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)
        has_permission = False

        # Verifica si el usuario actual tiene el permiso Administra roles
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[0]:
                has_permission = True

        return has_permission


class CheckAdminOrConsUsersPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        has_permission = False
        permissions = return_permissions(request.user)

        # Verifica si el usuario actual tiene los permisos Administra usuarios o Consulta usuarios 
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[5]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[1]:
                has_permission = True
        return has_permission


class CheckAdminUsersPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        has_permission = False
        permissions = return_permissions(request.user)

        # Verifica si el usuario actual tiene el permiso Administra usuarios
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[1]:
                has_permission = True

        return has_permission


class CheckAdminOrConsInmobPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene los permisos Administra inmobiliarias o Consulta inmobiliarias
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[6]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[2]:
                has_permission = True

        return has_permission


class CheckAdminInmobPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene el permiso Administra inmobiliarias
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[2]:
                has_permission = True

        return has_permission


class CheckAdminOrConsInmobOrConsParamPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene los permisos Administra inmobiliarias o Consulta inmobiliarias o Consulta parametros
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[6]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[2]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[10]:
                has_permission = True

        return has_permission


class CheckAdminOrConsParamPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene los permisos Administra parametros o Consulta parametros
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[10]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[11]:
                has_permission = True

        return has_permission


class CheckAdminParamPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene el permiso Administra parametros
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[11]:
                has_permission = True
        return has_permission


class CheckAdminInmobOrAdminParamPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene los permisos Administra inmobiliarias o Administra parametros
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[2]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[11]:
                has_permission = True

        return has_permission


class CheckAdminMoniOrConsProyectosPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene los permisos Administra proyectos o Consulta proyectos o
        # Monitorea proyectos
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[16]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[12]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[14]:
                has_permission = True

        return has_permission


class CheckAdminMoniProyectosPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene el permiso Administra proyectos 
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[12]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[14]:
                has_permission = True
        return has_permission


class CheckApproveProyectosPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene el permiso Aprueba proyectos 
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[13]:
                has_permission = True

        return has_permission


class CheckMonitorProyectosPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene el permiso Monitorea proyectos
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[14]:
                has_permission = True

        return has_permission


class CheckAdminOrConsCliPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene los permisos Administra clientes o Consulta clientes
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[12  ]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[16]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[17]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[18]:
                has_permission = True
        return has_permission


class CheckAdminCliPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene el permiso Administra clientes 
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[17]:
                has_permission = True

        return has_permission


class CheckAdminOrConsOrMoniProyectosPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene los permisos Administra clientes o Consulta clientes
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[12]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[14]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[16]:
                has_permission = True

        return has_permission


class CheckAdminOrVendedorOrMoniProyectosPermission(
        permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene los permisos Administra proyectos o Monitorea proyectos o Es vendedor
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[8]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[12]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[14]:
                has_permission = True

        return has_permission


class CheckAdminOrVendedorOrMoniOrConsProyectosPermission(
        permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene los permisos Administra proyectos o Es vendedor o Monitorea proyectos o
        # Consulta proyectos
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[8]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[12]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[14]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[16]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[20]:
                has_permission = True
        return has_permission
        
'''        
class CheckRecepcionaGarantiasProyectosPermission(
        permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE
    def has_permission(self, request, view):
        permissions = return_permissions(request.user)
        
        has_permission = False
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[20]:
                has_permission = True
        return has_permission        
'''

class CheckApproveInmueblesPermission(
        permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene el permiso Aprueba inmuebles
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[19]:
                has_permission = True

        return has_permission


class CheckAsistenteComercialPermission(
        permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene el permiso Es asistente comercial
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[9]:
                has_permission = True

        return has_permission


class CheckVendedorPermission(
        permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene el permiso Es vendedor
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[8]:
                has_permission = True

        return has_permission


class CheckAprobadorPermission(
        permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene el permiso Es aprobador inmobiliario
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[15]:
                has_permission = True

        return has_permission


class CheckRecepcionaGarantiasPermission(
        permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene el permiso Recepciona garantias
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[20]:
                has_permission = True

        return has_permission


class CheckApproveConfeccionPromesaPermission(
        permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        permissions = return_permissions(request.user)

        has_permission = False
        # Verifica si el usuario actual tiene el permiso Aprueba confeccion promesa
        for permission in permissions:
            if permission.Name == constants.PERMISSIONS[16]:
                has_permission = True
            if permission.Name == constants.PERMISSIONS[21]:
                has_permission = True    

        return has_permission


class CheckProyectoMarketingPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        project = Proyecto.objects.get(ProyectoID=view.kwargs.get('ProyectoID'))
        user = User.objects.get(Rut=request.user)
        user_project_types = UserProyecto.objects.filter(ProyectoID=project, UserID=user)
        project_type_valid = any([t.UserProyectoTypeID.Name == constants.USER_PROYECTO_TYPE[5] or
                                  t.UserProyectoTypeID.Name == constants.USER_PROYECTO_TYPE[1]
                                  for t in user_project_types])
        role_valid = any([role.Name == constants.UserRole.GERENTE_COMERCIAL for role in user.RoleID.all()])
        return project_type_valid or role_valid


class CheckProyectoLegalPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        project = Proyecto.objects.get(ProyectoID=view.kwargs.get('ProyectoID'))
        user = User.objects.get(Rut=request.user)
        user_project_types = UserProyecto.objects.filter(ProyectoID=project, UserID=user)
        project_type_valid = any([t.UserProyectoTypeID.Name == constants.USER_PROYECTO_TYPE[6] or
                                  t.UserProyectoTypeID.Name == constants.USER_PROYECTO_TYPE[1]
                                  for t in user_project_types])
        role_valid = any([role.Name == constants.UserRole.GERENTE_COMERCIAL for role in user.RoleID.all()])
        return project_type_valid or role_valid


class CheckProyectoFinazaPermission(permissions.BasePermission):
    message = constants.PERMISSION_MESSAGE

    def has_permission(self, request, view):
        project = Proyecto.objects.get(ProyectoID=request.data.get('ProyectoID'))
        user = User.objects.get(Rut=request.user)
        user_project_types = UserProyecto.objects.filter(ProyectoID=project, UserID=user)
        project_type_valid = any([t.UserProyectoTypeID.Name == constants.USER_PROYECTO_TYPE[7] or
                                  t.UserProyectoTypeID.Name == constants.USER_PROYECTO_TYPE[1]
                                  for t in user_project_types])
        role_valid = any([role.Name == constants.UserRole.GERENTE_COMERCIAL for role in user.RoleID.all()])
        return project_type_valid or role_valid

# Funciones para retornar datos segun permisos


def list_proyectos_by_permission(current_user):
    permissions = return_permissions(current_user)

    has_permission = False
    
    for permission in permissions:
        # Verifica si el usuario actual posee algunos de estos permisos: Administra proyectos, Monitorea proyectos,
        # Consulta proyectos o Aprueba inmuebles, si posee alguno se le muestran todos los proyectos
        if permission.Name == constants.PERMISSIONS[12]:
            queryset = Proyecto.objects.all()
            has_permission = True
        elif permission.Name == constants.PERMISSIONS[14]:
            queryset = Proyecto.objects.all()
            has_permission = True
        elif permission.Name == constants.PERMISSIONS[16]:
            has_permission = True
            queryset = Proyecto.objects.all()
        elif permission.Name == constants.PERMISSIONS[19]:
            has_permission = True
            queryset = Proyecto.objects.all()

    # Si no posee alguno de los permisos, se le muestran los proyectos en que esta asignado
    if not has_permission:
        queryset = Proyecto.objects.filter(
            UserProyecto__Rut=current_user
        )

    return queryset
