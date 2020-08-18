import re
import os
import random
import string
import calendar
import datetime
import math
import pandas as pd
from itertools import cycle
from decimal import Decimal
from builtins import setattr
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.exceptions import FieldDoesNotExist
from . import constants
from .models import UF, ConstantNumeric
from users.models import User, Permission
from empresas_and_proyectos.models.etapas import Etapa
from empresas_and_proyectos.models.inmuebles import Inmueble
from empresas_and_proyectos.models.proyectos import (
    ProyectoContactInfo,
    UserProyectoType,
    UserProyecto)
from ventas.models.cotizaciones import (
    Cotizacion,
    CotizacionInmueble)
from ventas.models.clientes import Cliente
from ventas.models.reservas import Reserva
from ventas.models.empleadores import Empleador
from ventas.models.empresas_compradoras import EmpresaCompradora
from ventas.models.patrimonies import Patrimony
from .generate_pdf import render_create_cotizacion_to_pdf, render_create_pre_approbation_to_pdf
from common import validations
from rest_framework import status


# Funcion para determinar si el rut es valido
def validar_rut(rut):
    rut = rut.upper()
    rut = rut.replace("-", "")
    rut = rut.replace(".", "")
    aux = rut[:-1]
    dv = rut[-1:]

    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido, factors))
    res = (-s) % 11

    if str(res) == dv:
        return True
    elif dv == "K" and res == 10:
        return True
    else:
        return False

# Funcion que verifica que la contraseña cumpla con los requisitos especificados: Minimo 7 caracteres,
# al menos 1 mayuscula y al menos 1 numero

def validar_contrasena(password):
    if len(password) >= 7 and re.search(
        '[0-9]',
        password) is not None and re.search(
        '[A-Z]',
            password) is not None:
        return True

# Funcion para agregar al rut los puntos y la coma


def formatear_rut(rut):
    actual = rut.replace("/^0+/", "")
    if actual is not '' and len(actual) > 1:
        rut_sin_formato = actual.replace(r"/\./g", "")
        actual_limpio = rut_sin_formato.replace("/-/g", "")
        inicio = actual_limpio[0:-1]
        rut_formateado = ""
        i = 0
        j = 1
        for i in reversed(inicio):
            rut_formateado = i + rut_formateado
            if j % 3 == 0 and j <= len(inicio) - 1:
                rut_formateado = "." + rut_formateado
            j = j + 1

        dv = actual_limpio[-1]
        rut_formateado = rut_formateado + "-" + dv

    return rut_formateado

# Generador de contraseña aleatoria.


def generar_contrasena():
    low_1 = random.SystemRandom().choice(string.ascii_lowercase)
    low_2 = random.SystemRandom().choice(string.ascii_lowercase)
    low_3 = random.SystemRandom().choice(string.ascii_lowercase)
    low_4 = random.SystemRandom().choice(string.ascii_lowercase)
    dig_1 = random.SystemRandom().choice(string.digits)
    dig_2 = random.SystemRandom().choice(string.digits)
    dig_3 = random.SystemRandom().choice(string.digits)
    dig_4 = random.SystemRandom().choice(string.digits)
    pwd = ""
    pwd = low_1 + low_2 + low_3 + low_4 + dig_1 + dig_2 + dig_3 + dig_4
    pwd = ''.join(random.sample(pwd, len(pwd)))

    return pwd


# Funcion que retorna un None si no encuentra el objeto dado un modelo y el atributo a buscar


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


# Funcion que retorna el valor actual de la uf


def valor_uf_actual():
    date = datetime.datetime.now()
    now = date.date()
    
    try:
        # uf = UF.objects.get(Date=now)
        uf = UF.objects.order_by('-Date').first()
    except UF.DoesNotExist:
        return Decimal()
    return uf.Value

# Funcion que verifica si viene algun campo en blanco en la plantilla de excel


def is_nan(value):
    try:
        return math.isnan(float(value))
    except BaseException:
        return False

# Funcion que retorna el url absoluto para los retornos de link de archivos


def get_full_path_x(request):
    full_path = ('http', ('', 's')[request.is_secure()], '://',
                 request.META['HTTP_HOST'])

    return ''.join(full_path)

# Funcion que retorna el usuario conectado


def return_current_user(self):
    current_user = User.objects.get(
        DjangoUser__username=self.context['request'].user)

    return current_user


# Funcion que retorna los permisos del usuario conectado


def return_permissions(user):
    permissions = Permission.objects.filter(
        permission_role__role_user__Rut=user
    ).distinct()

    return permissions

# Funcion para enviar la contraseña del usuario recien creado a su email


def enviar_contrasena_por_email(user, password):
    subject = 'Contraseña para inicio de sesión'
    message = render_to_string('generate_password.html', {
        'user': user,
        'password': password
    })

    # send_mail(
    #     subject,
    #     message,
    #     from_email=settings.EMAIL_HOST_USER,
    #     html_message=message,
    #     recipient_list=[
    #         user.Email])


# Funcion para enviar email a inmobiliaria

def send_email_to_inmobiliaria(subject, template, recipients, extra_data=None):
    for recipient in recipients:
        context_dict = {
            'user': recipient,
            'folio': extra_data['folio'],
            'name': extra_data['name']
        }
        message = render_to_string(template, context_dict)
        # send_mail(
        #     subject,
        #     message,
        #     from_email=settings.EMAIL_HOST_USER,
        #     html_message=message,
        #     recipient_list=[
        #         recipient.Email])


# Funcion para realizar el calculo del dividendo para el simulador de credito

def dividend_calculation(total_amount, percentage, rate, date):
    result = total_amount * (percentage / 100) * Decimal((math.pow(1 + rate / 100, 1 / 12) - 1)) * \
        Decimal((math.pow(1 + rate / 100, date) / (math.pow(1 + rate / 100, date) - 1)))
    return round(result, 2)


# Funcion para importar los nombres de las columnas del excel para crear inmuebles

def import_excel_inmuebles(file):
    file = pd.ExcelFile(file, header=None)

    data = file.parse(sheet_name='Inmuebles')
    
    columns = [
        'TipoInmueble',
        'Tipologia',
        'Edificio',
        'Numero',
        'Piso',
        'CantidadBanos',
        'CantidadHabitaciones',
        'MetrosCuadradosInterior',
        'MetrosCuadradosTerraza',
        'MetrosCuadradosLogia',
        'UsoyGoce',
        'Precio',
        'DescuentoMaximo',
        'Orientacion',
        'Estado']
    if "Cargar img de la Planta" in data.columns:
        columns.append('Planta')
    data.columns=columns
    return data


# Funcion para procesar los datos y retornar el pdf de la cotizacion a descargar
   
def download_pdf_views(cotizacion_id, letter_size, response=None):
    cotizacion = Cotizacion.objects.get(CotizacionID=cotizacion_id)
    contacts = ProyectoContactInfo.objects.filter(
        ProyectoID=cotizacion.ProyectoID)
    inmuebles_a_cotizar = CotizacionInmueble.objects.filter(
        CotizacionID=cotizacion).order_by("InmuebleID__InmuebleTypeID__id")

    total = 0
    total_uf = 0
    total_cuotas = 0
    departments_discount = 0
    total_without_discount = 0

    # Años para calcular dividendo
    plazo_8 = [8]
    plazo_10 = [10]
    plazo_15 = [15]
    plazo_20 = [20]
    plazo_25 = [25]
    plazo_30 = [30]

    valor_uf = valor_uf_actual
    tasa = get_or_none(
        ConstantNumeric,
        Name__iexact=constants.SEARCH_NAME_CONSTANT_NUMERIC[0])

    for cotizacion_inmueble in inmuebles_a_cotizar:
        if cotizacion_inmueble.Discount:
            price_discount = round(
                cotizacion_inmueble.InmuebleID.Price *
                cotizacion_inmueble.Discount /
                100,
                2)

            total_without_discount += cotizacion_inmueble.InmuebleID.Price
            
            price = cotizacion_inmueble.InmuebleID.Price - price_discount
            total_uf += price

            if inmueble.InmuebleTypeID.Name=='Departamento':
                departments_discount += price_discount
        else:
            total_uf += cotizacion_inmueble.InmuebleID.Price

    if cotizacion.CuotaID.all():
        for cuota in cotizacion.CuotaID.all():
            total_cuotas += cuota.Amount

        total_cuotas_solas = total_cuotas
        porcentaje_cuotas = total_cuotas * 100 / total_uf
        total += total_cuotas
    else:
        total_cuotas_solas = None
        porcentaje_cuotas = None

    # if cotizacion.PaymentFirmaPromesa:
    #     total += cotizacion.PaymentFirmaPromesa
    #     porcentaje_firma_promesa = cotizacion.PaymentFirmaPromesa * 100 / total_uf
    # else:
    #     porcentaje_firma_promesa = 0

    # porcentaje_firma_escritura = cotizacion.PaymentFirmaEscritura * 100 / total_uf
    porcentaje_firma_escritura = 0
    if cotizacion.PaymentFirmaEscritura:
        total += cotizacion.PaymentFirmaEscritura
        porcentaje_firma_escritura = (cotizacion.PaymentFirmaEscritura * 100) / total_uf
        
    porcentaje_firma_promesa = 0
    if cotizacion.PaymentFirmaPromesa:
        total += cotizacion.PaymentFirmaPromesa
        porcentaje_firma_promesa = (cotizacion.PaymentFirmaPromesa * 100) / total_uf

    porcentaje_subsidio = 0
    if cotizacion.Subsidio:
        total += cotizacion.Subsidio
        porcentaje_subsidio = (cotizacion.Subsidio * 100) / total_uf

    porcentaje_libreta = 0
    if cotizacion.Libreta:
        total += cotizacion.Libreta
        porcentaje_libreta = (cotizacion.Libreta * 100) / total_uf
    
    if cotizacion.PaymentInstitucionFinanciera:
        total += cotizacion.PaymentInstitucionFinanciera
        porcentaje_credito = cotizacion.PaymentInstitucionFinanciera * 100 / total_uf

        # 8 años
        # UF
        dividend = dividend_calculation(
            total, porcentaje_credito, tasa.Value, plazo_8[0])
        plazo_8.append(dividend)

        # Pesos
        multiply = round(dividend * valor_uf_actual(), 0)
        dividend_pesos = "{:,}".format(multiply).replace(',', '.')
        plazo_8.append(dividend_pesos)

        # Renta Pesos
        rent = 4 * dividend
        multiply = round(rent * valor_uf_actual(), 0)
        dividend_pesos = "{:,}".format(multiply).replace(',', '.')
        plazo_8.append(dividend_pesos)

        # 10 años
        # UF
        dividend = dividend_calculation(
            total, porcentaje_credito, tasa.Value, plazo_10[0])
        plazo_10.append(dividend)

        # Pesos
        multiply = round(dividend * valor_uf_actual(), 0)
        dividend_pesos = "{:,}".format(multiply).replace(',', '.')
        plazo_10.append(dividend_pesos)

        # Renta Pesos
        rent = 4 * dividend
        multiply = round(rent * valor_uf_actual(), 0)
        dividend_pesos = "{:,}".format(multiply).replace(',', '.')
        plazo_10.append(dividend_pesos)
        
        # 15 años
        # UF
        dividend = dividend_calculation(
            total, porcentaje_credito, tasa.Value, plazo_15[0])
        plazo_15.append(dividend)

        # Pesos
        multiply = round(dividend * valor_uf_actual(), 0)
        dividend_pesos = "{:,}".format(multiply).replace(',', '.')
        plazo_15.append(dividend_pesos)

        # Renta Pesos
        rent = 4 * dividend
        multiply = round(rent * valor_uf_actual(), 0)
        dividend_pesos = "{:,}".format(multiply).replace(',', '.')
        plazo_15.append(dividend_pesos)

        # 20 años
        # UF
        dividend = dividend_calculation(
            total, porcentaje_credito, tasa.Value, plazo_20[0])
        plazo_20.append(dividend)

        # Pesos
        multiply = round(dividend * valor_uf_actual(), 0)
        dividend_pesos = "{:,}".format(multiply).replace(',', '.')
        plazo_20.append(dividend_pesos)

        # Renta Pesos
        rent = 4 * dividend
        multiply = round(rent * valor_uf_actual(), 0)
        dividend_pesos = "{:,}".format(multiply).replace(',', '.')
        plazo_20.append(dividend_pesos)

        # 25 años
        # UF
        dividend = dividend_calculation(
            total, porcentaje_credito, tasa.Value, plazo_25[0])
        plazo_25.append(dividend)

        # Pesos
        multiply = round(dividend * valor_uf_actual(), 0)
        dividend_pesos = "{:,}".format(multiply).replace(',', '.')
        plazo_25.append(dividend_pesos)

        # Renta Pesos
        rent = 4 * dividend
        multiply = round(rent * valor_uf_actual(), 0)
        dividend_pesos = "{:,}".format(multiply).replace(',', '.')
        plazo_25.append(dividend_pesos)

        # 30 años
        # UF
        dividend = dividend_calculation(
            total, porcentaje_credito, tasa.Value, plazo_30[0])
        plazo_30.append(dividend)

        # Pesos
        multiply = round(dividend * valor_uf_actual(), 0)
        dividend_pesos = "{:,}".format(multiply).replace(',', '.')
        plazo_30.append(dividend_pesos)

        # Renta Pesos
        rent = 4 * dividend
        multiply = round(rent * valor_uf_actual(), 0)
        dividend_pesos = "{:,}".format(multiply).replace(',', '.')
        plazo_30.append(dividend_pesos)
    else:
        porcentaje_credito = 0

    if cotizacion.AhorroPlus:
        total += cotizacion.AhorroPlus
        porcentaje_ahorro = cotizacion.AhorroPlus * 100 / total_uf
    else:
        porcentaje_ahorro = 0
    
    # Datos para renderizar a pdf
    context_dict = {
        'Folio': cotizacion.Folio,
        'proyecto': cotizacion.ProyectoID,
        'cuotas_data': cotizacion.CuotaID.all,
        'inmuebles_a_cotizar': inmuebles_a_cotizar,
        'uf': valor_uf,
        'total': total_uf,
        'total_pago': total,
        'total_cuotas': total_cuotas_solas,
        'total_firma_promesa': cotizacion.PaymentFirmaPromesa,
        'total_firma_escritura': cotizacion.PaymentFirmaEscritura,
        'total_subsidio': cotizacion.Subsidio,
        'total_libreta': cotizacion.Libreta,
        'total_credito': cotizacion.PaymentInstitucionFinanciera,
        'total_departments_discount': departments_discount,
        'porcentaje_departments_discount': round(departments_discount / total_without_discount * 100, 2),
        'ahorro_plus': cotizacion.AhorroPlus,
        'date_firma_promesa': cotizacion.DateFirmaPromesa,
        'porcentaje_cuotas': porcentaje_cuotas,
        'porcentaje_firma_promesa': porcentaje_firma_promesa,
        'porcentaje_firma_escritura': porcentaje_firma_escritura,
        'porcentaje_subsidio':porcentaje_subsidio,
        'porcentaje_libreta':porcentaje_libreta,
        'porcentaje_credito': porcentaje_credito,
        'porcentaje_ahorro': porcentaje_ahorro,
        'porcentaje_tasa': tasa.Value,
        'plazo_8': plazo_8,
        'plazo_10': plazo_10,
        'plazo_15': plazo_15,
        'plazo_20': plazo_20,
        'plazo_25': plazo_25,
        'plazo_30': plazo_30,
        'nombre_empresa': constants.COMPANY_NAME[0],
        'contactos': contacts,
        'tamaño_letra': letter_size
    }
    pdf = render_create_cotizacion_to_pdf(context_dict, response)
    name = "%s_COT" % (cotizacion.Folio)
    
    return {'name':name, 'pdf':pdf}


def download_pre_approbation_views(reserva_id, letter_size, response):
    reserva = Reserva.objects.get(ReservaID=reserva_id)
    empleador = Empleador.objects.filter(ClienteID=reserva.ClienteID)
    if len(empleador) > 0:
        empleador = empleador[0]
    else:
        empleador = Empleador()
    empresa_compradora = EmpresaCompradora.objects.filter(ClienteID=reserva.ClienteID)
    if len(empresa_compradora) > 0:
        empresa_compradora = empresa_compradora[0]
    else:
        empresa_compradora = EmpresaCompradora()
    client = Cliente.objects.filter(UserID=reserva.ClienteID.UserID)
    if len(client) > 0:
        client = client[0]
    else:
        client = Cliente()
    if 'VariableSalary' in client.Extra['Values']:
        variableSalary = client.Extra['Values']['VariableSalary']
    else:
        variableSalary = 0
    total_liquid = int(client.Extra['Values']['LiquidIncome']) + int(variableSalary) + int(client.Extra['Values']['Honoraries'])
    patrimony = Patrimony.objects.get(ClienteID=reserva.ClienteID)
    total_activos = patrimony.RealState + patrimony.CreditoHipotecario['PagosMensuales'] + patrimony.Vehicle + patrimony.DownPayment + patrimony.Other
    total_pasivos = patrimony.CreditCard['Pasivos'] + patrimony.CreditoConsumo['Pasivos'] + patrimony.PrestamoEmpleador['Pasivos'] + patrimony.DeudaIndirecta['Pasivos'] + patrimony.AnotherCredit['Pasivos'] + patrimony.CreditoComercio['Pasivos']
    context_dict = {
        'reserva': reserva,
        'empleador': empleador,
        'empresa_compradora': empresa_compradora,
        'client': client,
        'total_liquid': total_liquid,
        'total_activos': total_activos,
        'total_pasivos': total_pasivos,
        'patrimony': patrimony,
        'tamaño_letra': letter_size
    }
    pdf = render_create_pre_approbation_to_pdf(context_dict, response)
    name = "%s_COT" % (reserva.Folio)
    return name

# Funcion para crear relacion entre inmueble y orientacion
def crear_relacion(_ThroughModel, orientation_lab, orientacion,
                   inmueble_lab, inmueble):
    through = _ThroughModel()
    setattr(through, orientation_lab, orientacion)
    setattr(through, inmueble_lab, inmueble)


def agregar_orientaciones_inmueble(orientaciones, inmueble, sentidos,
                                   throug_list, _ThroughModel):
    norte = sentidos.get(Name="Norte")
    sur = sentidos.get(Name="Sur")
    oriente = sentidos.get(Name="Oriente")
    poniente = sentidos.get(Name="Poniente")
    orientation_lab = 'orientation'
    inmueble_lab = 'inmueble'

    try:
        inmueble_lab = _ThroughModel._meta.get_field('historicalinmueble')
        return
    except FieldDoesNotExist:
        pass

    if orientaciones == constants.ORIENTACIONES[0]:
        pass
    elif orientaciones == constants.ORIENTACIONES[1]:
        throug_list += [
            crear_relacion(_ThroughModel, orientation_lab, norte,
                           inmueble_lab, inmueble)
        ]
    elif orientaciones == constants.ORIENTACIONES[2]:
        throug_list += [
            crear_relacion(_ThroughModel, orientation_lab, norte,
                           inmueble_lab, inmueble),
            crear_relacion(_ThroughModel, orientation_lab, oriente,
                           inmueble_lab, inmueble)
        ]

    elif orientaciones == constants.ORIENTACIONES[3]:
        throug_list += [
            crear_relacion(_ThroughModel, orientation_lab, norte,
                           inmueble_lab, inmueble),
            crear_relacion(_ThroughModel, orientation_lab, poniente,
                           inmueble_lab, inmueble)
        ]

    elif orientaciones == constants.ORIENTACIONES[4]:
        throug_list += [
            crear_relacion(_ThroughModel, orientation_lab, norte,
                           inmueble_lab, inmueble),
            crear_relacion(_ThroughModel, orientation_lab, sur,
                           inmueble_lab, inmueble)
        ]

    elif orientaciones == constants.ORIENTACIONES[5]:
        throug_list += [
            crear_relacion(_ThroughModel, orientation_lab, oriente,
                           inmueble_lab, inmueble)]

    elif orientaciones == constants.ORIENTACIONES[6]:
        throug_list += [
            crear_relacion(_ThroughModel, orientation_lab, oriente,
                           inmueble_lab, inmueble),
            crear_relacion(_ThroughModel, orientation_lab, poniente,
                           inmueble_lab, inmueble)
        ]

    elif orientaciones == constants.ORIENTACIONES[7]:
        throug_list += [
            crear_relacion(_ThroughModel, orientation_lab, poniente,
                           inmueble_lab, inmueble)]

    elif orientaciones == constants.ORIENTACIONES[8]:
        throug_list += [
            crear_relacion(_ThroughModel, orientation_lab, sur,
                           inmueble_lab, inmueble)]

    elif orientaciones == constants.ORIENTACIONES[9]:
        throug_list += [
            crear_relacion(_ThroughModel, orientation_lab, sur,
                           inmueble_lab, inmueble),
            crear_relacion(_ThroughModel, orientation_lab, oriente,
                           inmueble_lab, inmueble)
        ]

    elif orientaciones == constants.ORIENTACIONES[10]:
        throug_list += [
            crear_relacion(_ThroughModel, orientation_lab, sur,
                           inmueble_lab, inmueble),
            crear_relacion(_ThroughModel, orientation_lab, poniente,
                           inmueble_lab, inmueble)
        ]

    elif orientaciones == constants.ORIENTACIONES[11]:
        throug_list += [
            crear_relacion(_ThroughModel, orientation_lab, oriente,
                           inmueble_lab, inmueble),
            crear_relacion(_ThroughModel, orientation_lab, norte,
                           inmueble_lab, inmueble),
            crear_relacion(_ThroughModel, orientation_lab, poniente,
                           inmueble_lab, inmueble)
        ]

    elif orientaciones == constants.ORIENTACIONES[12]:
        throug_list += [
            crear_relacion(_ThroughModel, orientation_lab, norte,
                           inmueble_lab, inmueble),
            crear_relacion(_ThroughModel, orientation_lab, oriente,
                           inmueble_lab, inmueble),
            crear_relacion(_ThroughModel, orientation_lab, sur,
                           inmueble_lab, inmueble)
        ]
    else:
        throug_list += [
            crear_relacion(_ThroughModel, orientation_lab, norte,
                           inmueble_lab, inmueble),
            crear_relacion(_ThroughModel, orientation_lab, poniente,
                           inmueble_lab, inmueble),
            crear_relacion(_ThroughModel, orientation_lab, sur,
                           inmueble_lab, inmueble)
        ]


def verify_data_proyecto(proyecto):
    # Tipos de Usuarios
    asistente_comercial_type = UserProyectoType.objects.get(
        Name=constants.USER_PROYECTO_TYPE[3])
    vendedores_type = UserProyectoType.objects.get(
        Name=constants.USER_PROYECTO_TYPE[2])
    representantes_type = UserProyectoType.objects.get(
        Name=constants.USER_PROYECTO_TYPE[0])
    aprobadores_type = UserProyectoType.objects.get(
        Name=constants.USER_PROYECTO_TYPE[4])

    # Usuarios
    asistentes = UserProyecto.objects.filter(
        ProyectoID=proyecto,
        UserProyectoTypeID=asistente_comercial_type).values_list('UserID')
    vendedores = UserProyecto.objects.filter(
        ProyectoID=proyecto,
        UserProyectoTypeID=vendedores_type).values_list('UserID')
    representantes = UserProyecto.objects.filter(
        ProyectoID=proyecto,
        UserProyectoTypeID=representantes_type).values_list('UserID')
    aprobadores = UserProyecto.objects.filter(
        ProyectoID=proyecto,
        UserProyectoTypeID=aprobadores_type).values_list('UserID')

    # Etapas
    etapas = Etapa.objects.filter(ProyectoID=proyecto)
    if etapas:
        for etapa in etapas:
            inmuebles = Inmueble.objects.filter(EtapaID=etapa)
            if not inmuebles:
                raise validations.CustomValidation(
                    "Falta agregar inmuebles",
                    status_code=status.HTTP_409_CONFLICT)

    if proyecto.ConstructoraID.RazonSocial == 'Pendiente':
        raise validations.CustomValidation(
            "Falta agregar constructora",
            status_code=status.HTTP_409_CONFLICT)

    if proyecto.ProyectoAseguradoraID and proyecto.ProyectoAseguradoraID.AseguradoraID.Name == 'Pendiente':
        raise validations.CustomValidation(
            "Falta agregar aseguradora",
            status_code=status.HTTP_409_CONFLICT)

    if not asistentes.exists():
        raise validations.CustomValidation(
            "Falta agregar asistente(s) comercial(es)",
            status_code=status.HTTP_409_CONFLICT)

    if not vendedores.exists():
        raise validations.CustomValidation(
            "Falta agregar vendedor(es)", status_code=status.HTTP_409_CONFLICT)

    if not representantes.exists():
        raise validations.CustomValidation(
            "Falta agregar representante(s)",
            status_code=status.HTTP_409_CONFLICT)

    if not aprobadores.exists():
        raise validations.CustomValidation(
            "Falta agregar aprobador(es)",
            status_code=status.HTTP_409_CONFLICT)
