from decimal import Decimal
from common.services import dividend_calculation
from django.template.defaultfilters import slugify

# Funcion para calcular el patrimonio a incluir en la ficha de preaprobacion


def calculate_totals_patrimony(patrimony):
    total_activos = patrimony.RealState + patrimony.Vehicle + patrimony.DownPayment + patrimony.Other

    total_pasivos = (patrimony.CreditCard['Pasivos'] + patrimony.CreditoConsumo['Pasivos'] +
                     patrimony.CreditoHipotecario['Pasivos'] + patrimony.PrestamoEmpleador['Pasivos'] +
                     patrimony.CreditoComercio['Pasivos'] + patrimony.DeudaIndirecta['Pasivos'] +
                     patrimony.AnotherCredit['Pasivos'])

    total_pagos = (patrimony.CreditCard['PagosMensuales'] + patrimony.CreditoConsumo['PagosMensuales'] +
                   patrimony.CreditoHipotecario['PagosMensuales'] + patrimony.PrestamoEmpleador['PagosMensuales'] +
                   patrimony.CreditoComercio['PagosMensuales'] + patrimony.DeudaIndirecta['PagosMensuales'] +
                   patrimony.AnotherCredit['PagosMensuales'])

    total_saldos = (patrimony.CreditCard['Saldo'] + patrimony.CreditoConsumo['Saldo'] +
                    patrimony.CreditoHipotecario['Saldo'] + patrimony.PrestamoEmpleador['Saldo'] +
                    patrimony.CreditoComercio['Saldo'] + patrimony.DeudaIndirecta['Saldo'] +
                    patrimony.AnotherCredit['Saldo'])

    totals = {
        "total_activos": total_activos,
        "total_pasivos": total_pasivos,
        "total_pagos": total_pagos,
        "total_saldos": total_saldos
    }

    return totals


def calculate_simulate_values(total_amount, percentage, rate, date, codeudor):
    desgravamen_insurance = 0
    dividend_uf = 0

    if percentage:
        if codeudor:
            desgravamen_insurance = total_amount * (percentage / 100) * Decimal(0.00028) * 2
        else:
            desgravamen_insurance = total_amount * (percentage / 100) * Decimal(0.00028)
        
        dividend_uf = dividend_calculation(total_amount, percentage, rate, date)

    fire_quake_insurance = total_amount * Decimal(0.000245)

    dividend_insurances = round(dividend_uf + desgravamen_insurance + fire_quake_insurance, 2)

    min_rent = 4 * dividend_uf + desgravamen_insurance + fire_quake_insurance

    values = {
        'desgravamen_insurance': desgravamen_insurance,
        'fire_quake_insurance': fire_quake_insurance,
        'dividend_uf': dividend_uf,
        'dividend_insurances': dividend_insurances,
        'min_rent': min_rent
    }

    return values


def add_document(name, required=False):
    document = dict()

    document['title'] = name
    document['name'] = slugify(name)
    document['required'] = required

    return document


def return_required_documents():
    documents_required = list()

    cotizacion = add_document('Cotización', True)
    certificado_matrimonio = add_document('Certificado matrimonio', False)
    constitucion_sociedad = add_document('Constitución sociedad', False)
    pago_garantia = add_document('Pago garantía', True)
    fotocopia_carnet = add_document('Fotocopia carnet', True)
    liquidacion_1 = add_document('Última liquidación 1', False)
    liquidacion_2 = add_document('Última liquidación 2', False)
    liquidacion_3 = add_document('Última liquidación 3', False)
    cotizacion_afp = add_document('Último año de cotizaciones AFP', False)

    documents_required.extend((cotizacion, certificado_matrimonio, constitucion_sociedad, pago_garantia,
                               fotocopia_carnet, liquidacion_1, liquidacion_2, liquidacion_3,
                               cotizacion_afp))
    return documents_required
