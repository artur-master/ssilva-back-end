from django.utils.encoding import force_text
from . import constants, services
from empresas_and_proyectos.models.inmobiliarias import Inmobiliaria
from empresas_and_proyectos.models.inmuebles import InmuebleType
from users.models import User, Role
from ventas.models.empresas_compradoras import EmpresaCompradora
from ventas.models.empleadores import Empleador
from rest_framework import status
from rest_framework.exceptions import APIException

# Clase para retornar validaciones customizables


class CustomValidation(APIException):
    def __init__(self, detail, field=None, status_code=None):
        self.status_code = status_code
        self.detail = {'detail': force_text(detail)}

# Funciones de validacion 

def validate_rut_empresa(value):
    inmobiliaria = Inmobiliaria.objects.filter(Rut=value)
    if inmobiliaria.exists():
        raise CustomValidation(
            'Rut ingresado ya existe en el sistema',
            status_code=status.HTTP_409_CONFLICT)


def validate_rut_empleador(value):
    empleador = Empleador.objects.filter(Rut=value)
    if empleador.exists():
        raise CustomValidation(
            'Rut ingresado ya existe en el sistema',
            status_code=status.HTTP_409_CONFLICT)


def validate_rut_empresa_compradora(value):
    empresa_compradora = EmpresaCompradora.objects.filter(Rut=value)
    if empresa_compradora.exists():
        raise CustomValidation(
            'Rut ingresado ya existe en el sistema',
            status_code=status.HTTP_409_CONFLICT)


def validate_rut_usuario(value):
    user = User.objects.filter(Rut=value)
    if user.exists():
        raise CustomValidation(
            'Rut ingresado ya existe en el sistema',
            status_code=status.HTTP_409_CONFLICT)


def validate_name_empresa(value):
    inmobiliaria = Inmobiliaria.objects.filter(RazonSocial=value)
    if inmobiliaria.exists():
        raise CustomValidation(
            'Razón Social ingresada ya existe en el sistema',
            status_code=status.HTTP_409_CONFLICT)


def validate_name_role(value):
    role = Role.objects.filter(Name=value)
    if role.exists():
        raise CustomValidation(
            'Nombre ingresado ya existe en el sistema',
            status_code=status.HTTP_409_CONFLICT)

# Funciones para validar que las restricciones de los inmuebles estan correctas, es decir, no hayan restri
# cciones repetidas

def revisar_restricciones(restrictions_data):
    restrictions_uuid = []

    for restriction_data in restrictions_data:
        inmueble_uuid = str(restriction_data['InmuebleBID'])
        restrictions_uuid.append(inmueble_uuid)

    for uuid in restrictions_uuid:
        for uuid_next in restrictions_uuid[restrictions_uuid.index(uuid) + 1:]:
            if uuid == uuid_next:
                raise CustomValidation(
                    "Restricciones inconsistentes",
                    status_code=status.HTTP_409_CONFLICT)


def recorrer_arreglos_numeros_duplicados(arreglo, tipo_inmueble, edificio):
    if arreglo:
        for numero in arreglo:
            for numero_next in arreglo[arreglo.index(numero) + 1:]:
                if numero == numero_next:
                    if edificio:
                        message = "%s del edificio %s no pueden tener el mismo número" % (
                            tipo_inmueble, edificio.Name)
                    else:
                        message = "%s no pueden tener el mismo número" % (
                            tipo_inmueble)
                    raise CustomValidation(
                        message, status_code=status.HTTP_409_CONFLICT)


def revisar_numeros_duplicados(inmuebles_data, edificio):
    numeros_deptos = []
    numeros_bodegas = []
    numeros_estacionamiento = []
    numeros_casa = []

    for inmueble_data in inmuebles_data:
        inmueble_type = InmuebleType.objects.get(
            InmuebleTypeID=inmueble_data['InmuebleTypeID'])

        if inmueble_type.Name == constants.INMUEBLE_TYPE[0]:
            numeros_deptos.append(inmueble_data['Number'])

        if inmueble_type.Name == constants.INMUEBLE_TYPE[1]:
            numeros_bodegas.append(inmueble_data['Number'])

        if inmueble_type.Name == constants.INMUEBLE_TYPE[2]:
            numeros_estacionamiento.append(inmueble_data['Number'])

        if inmueble_type.Name == constants.INMUEBLE_TYPE[3]:
            numeros_casa.append(inmueble_data['Number'])

    if edificio:
        recorrer_arreglos_numeros_duplicados(
            numeros_deptos, "Departamentos", edificio)
        recorrer_arreglos_numeros_duplicados(
            numeros_bodegas, "Bodegas", edificio)
        recorrer_arreglos_numeros_duplicados(
            numeros_estacionamiento, "Estacionamientos", edificio)
    else:
        recorrer_arreglos_numeros_duplicados(numeros_casa, "Casas", None)


def recorrer_arreglos_numeros_duplicados_excel(arreglo, tipo_inmueble):
    if arreglo:
        for inmueble in arreglo:
            for inmueble_next in arreglo[arreglo.index(inmueble) + 1:]:
                if inmueble['edificio']:
                    if inmueble['edificio'] == inmueble_next['edificio']:
                        if inmueble['numero'] == inmueble_next['numero']:
                            message = "%s del edificio %s no pueden tener el mismo número" % (
                                tipo_inmueble, depto['edificio'])
                            raise CustomValidation(
                                message, status_code=status.HTTP_409_CONFLICT)
                else:
                    if inmueble['numero'] == inmueble_next['numero']:
                        message = "%s no pueden tener el mismo número" % (
                            tipo_inmueble)
                        raise CustomValidation(
                            message, status_code=status.HTTP_409_CONFLICT)


def revisar_numeros_duplicados_excel(inmuebles):
    inmuebles = list(inmuebles)
    for inmueble in inmuebles:
        if services.is_nan(inmueble.Edificio):
            for inmueble_next in inmuebles[inmuebles.index(inmueble) + 1:]:
                if inmueble.TipoInmueble == inmueble_next.TipoInmueble:
                    if inmueble.Numero == inmueble_next.Numero:
                        message = "Inmuebles del tipo %s no pueden tener el mismo número" % (
                            inmueble.TipoInmueble.lower())
                        raise CustomValidation(
                            message, status_code=status.HTTP_409_CONFLICT)
        else:
            for inmueble_next in inmuebles[inmuebles.index(inmueble) + 1:]:
                if inmueble.Edificio == inmueble_next.Edificio:
                    if inmueble.TipoInmueble == inmueble_next.TipoInmueble:
                        if inmueble.Numero == inmueble_next.Numero:
                            message = "Inmuebles del tipo %s pertenecientes al edificio %s no pueden tener el mismo número" % (
                                inmueble.TipoInmueble.lower(), inmueble.Edificio)
                            raise CustomValidation(
                                message, status_code=status.HTTP_409_CONFLICT)
