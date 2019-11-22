from django.contrib import admin
from ventas.models.clientes import (
    Cliente,
    ClienteProyecto,
    ClienteContactInfo)
from ventas.models.cotizaciones import (
    CotizacionType,
    CotizacionState,
    Cotizacion,
    CotizacionInmueble)
from ventas.models.facturas import Factura, FacturaInmueble, ComisionInmobiliaria
from ventas.models.reservas import (
    Reserva,
    ReservaInmueble,
    ReservaState)
from ventas.models.finding_contact import (
    FindingType,
    ContactMethodType)
from ventas.models.payment_forms import (
    Cuota,
    PayType,
    PreAprobacionCredito)
from ventas.models.ventas_logs import (
    VentaLog,
    VentaLogType)
from ventas.models.counter_folios import CounterFolio
from ventas.models.documents import DocumentVenta
from ventas.models.conditions import Condition
from ventas.models.empleadores import Empleador
from ventas.models.empresas_compradoras import EmpresaCompradora
from ventas.models.ofertas import Oferta
from ventas.models.patrimonies import Patrimony
from ventas.models.promesas import Promesa, PromesaInmueble


class FindingTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'FindingTypeID')


class CotizacionTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'CotizacionTypeID')


class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('ProyectoID', 'CotizacionTypeID', 'pk',
                    'CotizacionID')


class ConditionAdmin(admin.ModelAdmin):
    list_display = ('Description', 'pk', 'ConditionID')


class ContactMethodTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'ContactMethodTypeID')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('Description', 'pk', 'GenreID')


class CivilStatusAdmin(admin.ModelAdmin):
    list_display = ('Description', 'pk', 'CivilStatusID')


class EmpleadorAdmin(admin.ModelAdmin):
    list_display = ('RazonSocial', 'pk', 'EmpleadorID')


class ContractMarriageTypeAdmin(admin.ModelAdmin):
    list_display = ('Description', 'pk', 'ContractMarriageTypeID')


class PayTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'PayTypeID')


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('Name', 'LastNames', 'pk',
                    'UserID')


class ReservaAdmin(admin.ModelAdmin):
    list_display = ('ProyectoID', 'ReservaStateID', 'PayTypeID',
                    'pk', 'ReservaID')


class OfertaAdmin(admin.ModelAdmin):
    list_display = ('ProyectoID', 'OfertaState', 'PayTypeID',
                    'pk', 'OfertaID')


class PreAprobacionCreditoAdmin(admin.ModelAdmin):
    list_display = ('InstitucionFinanciera', 'Result', 'pk',
                    'PreAprobacionCreditoID')


class PromesaAdmin(admin.ModelAdmin):
    list_display = ('ProyectoID', 'PromesaState', 'PayTypeID',
                    'pk', 'PromesaID')


class FacturaAdmin(admin.ModelAdmin):
    list_display = ('InmobiliariaID', 'FacturaState', 'ProyectoID',
                    'pk', 'FacturaID')


class FacturaInmuebleAdmin(admin.ModelAdmin):
    list_display = ('InmuebleID', 'State', 'ProyectoID',
                    'pk')


class ComisionInmobiliariaAdmin(admin.ModelAdmin):
    list_display = ('ProyectoID', 'PromesaFirmada', 'EscrituraFirmada', 'CierreGestion',
                    'pk')


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(FindingType, FindingTypeAdmin)
admin.site.register(ClienteProyecto)
admin.site.register(ContactMethodType, ContactMethodTypeAdmin)
admin.site.register(CotizacionType, CotizacionTypeAdmin)
admin.site.register(CotizacionState)
admin.site.register(Cuota)
admin.site.register(CounterFolio)
admin.site.register(Cotizacion, CotizacionAdmin)
admin.site.register(CotizacionInmueble)
admin.site.register(ClienteContactInfo)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(ReservaInmueble)
admin.site.register(ReservaState)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(EmpresaCompradora)
admin.site.register(VentaLog)
admin.site.register(VentaLogType)
admin.site.register(Empleador, EmpleadorAdmin)
admin.site.register(PayType, PayTypeAdmin)
admin.site.register(Oferta, OfertaAdmin)
admin.site.register(PreAprobacionCredito, PreAprobacionCreditoAdmin)
admin.site.register(DocumentVenta)
admin.site.register(Patrimony)
admin.site.register(Promesa, PromesaAdmin)
admin.site.register(PromesaInmueble)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(FacturaInmueble, FacturaInmuebleAdmin)
admin.site.register(ComisionInmobiliaria, ComisionInmobiliariaAdmin)