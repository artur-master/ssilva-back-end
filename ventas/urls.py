from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from ventas.views.begin_ventas import BeginVentaViewSet
from ventas.views.clientes import ClienteViewSet
from ventas.views.cotizaciones import (
    CotizacionViewSet,
    DownloadCotizacionProyectoViewSet,
    CotizacionProyectoViewSet,
    CotizacionesClienteViewSet,
    CotizacionesCotizadorViewSet,
    CotizacionTypeViewSet)
from ventas.views.facturas import (
    ComisionInmobiliariaViewSet,
    UpdateComisionesAPIView,
    FacturaInmuebleViewSet,
    FacturaViewSet,
    DownloadFacturaViewSet,
    DownloadNotaCreditoViewSet, RegisterSendFacturaViewSet, RegisterDatePagoFacturaViewSet)
from ventas.views.finding_contact import (
    FindingTypeViewSet,
    ContactMethodTypeViewSet)
from ventas.views.ofertas import (
    OfertaViewSet,
    SendOfertaApproveInmobiliariaViewSet,
    ApproveInmobiliariaViewSet,
    RegisterReceptionGuaranteeViewSet,
    RegisterInstitucionFinancieraViewSet,
    ListPreAprobacionCreditoViewSet,
    RegisterResultPreAprobacionViewSet,
    ApproveConfeccionPromesaViewSet,
    ApproveUpdateOfertaViewSet,
    CancelOfertaViewSet)
from ventas.views.reservas import (
    ReservaViewSet,
    CancelReservaViewSet,
    SendControlReservaViewSet,
    ApproveControlReservaViewSet,
    UploadDocumentsReservaViewSet)
from ventas.views.utils import (
    UtilsClientesViewSet,
    UtilsCotizacionViewSet,
    GenerateCheckViewSet,
    RequiredDocumentsViewSet, UtilsPaymentViewSet)
from ventas.views.ventas_logs import (
    VentaLogViewSet,
    VentaLogClienteViewSet,
    VentaLogVendedorViewSet)
from ventas.views.promesas import (
    PromesaViewSet,
    ApproveMaquetaPromesaViewSet,
    ApproveControlPromesaViewSet,
    RegisterSendPromesaToInmobiliariaViewSet,
    RegisterSignatureInmobiliariaViewSet,
    LegalizePromesaViewSet,
    SendCopiesViewSet)

router = DefaultRouter()

router.register('clientes', ClienteViewSet)
router.register('cotizaciones', CotizacionViewSet)
router.register('cotizaciones-download', DownloadCotizacionProyectoViewSet)
router.register(
    'cotizaciones-proyectos',
    CotizacionProyectoViewSet,
    base_name='cotizaciones-proyectos')
router.register(
    'cotizaciones-cliente',
    CotizacionesClienteViewSet,
    base_name='cotizaciones-cliente')
router.register(
    'cotizaciones-cotizador',
    CotizacionesCotizadorViewSet,
    base_name='cotizaciones-cotizador')
router.register('reservas', ReservaViewSet)
router.register(
    'reservas-cancel',
    CancelReservaViewSet)
router.register(
    'reservas-send-control',
    SendControlReservaViewSet)
router.register(
    'reservas-approve-control',
    ApproveControlReservaViewSet)
router.register('ofertas', OfertaViewSet)
router.register(
    'ofertas-send-control',
    SendOfertaApproveInmobiliariaViewSet)
router.register(
    'ofertas-inmobiliarias-approve-control',
    ApproveInmobiliariaViewSet)
router.register(
    'ofertas-register-guarantee',
    RegisterReceptionGuaranteeViewSet)
router.register(
    'ofertas-register-instituciones-financieras',
    RegisterInstitucionFinancieraViewSet)
router.register(
    'ofertas-pre-aprobaciones',
    ListPreAprobacionCreditoViewSet)
router.register(
    'ofertas-register-result-pre-aprobaciones',
    RegisterResultPreAprobacionViewSet)
router.register(
    'ofertas-approve-confeccion-promesa',
    ApproveConfeccionPromesaViewSet)
router.register('ofertas-cancel', CancelOfertaViewSet)
router.register(
    'ofertas-approve-modificar',
    ApproveUpdateOfertaViewSet)
    
router.register('logs',
                VentaLogViewSet,
                base_name='logs')
router.register('logs-clientes',
                VentaLogClienteViewSet,
                base_name='logs-clientes')
router.register('logs-vendedores',
                VentaLogVendedorViewSet,
                base_name='logs-vendedores')
                
router.register('promesas', PromesaViewSet)
router.register(
    'promesas-approve-maqueta',
    ApproveMaquetaPromesaViewSet)
router.register(
    'promesas-approve-control',
    ApproveControlPromesaViewSet)
router.register(
    'promesas-register-send',
    RegisterSendPromesaToInmobiliariaViewSet)
router.register(
    'promesas-register-signature',
    RegisterSignatureInmobiliariaViewSet)
router.register(
    'promesas-legalize',
    LegalizePromesaViewSet)
router.register(
    'promesas-send-copies',
    SendCopiesViewSet)
router.register('finding-types', FindingTypeViewSet)
router.register('cotizacion-types', CotizacionTypeViewSet)
router.register('contact-method-types', ContactMethodTypeViewSet)
router.register('begin', BeginVentaViewSet)
router.register('upload-documents', UploadDocumentsReservaViewSet)
router.register('comisiones', ComisionInmobiliariaViewSet)
router.register('facturas', FacturaViewSet)
router.register('facturas-inmuebles',
                FacturaInmuebleViewSet,
                base_name='facturas-inmuebles')
router.register('facturas-download', DownloadFacturaViewSet)
router.register('facturas-nota-credito-download', DownloadNotaCreditoViewSet)
router.register('facturas-register-send', RegisterSendFacturaViewSet)
router.register('facturas-register-payment', RegisterDatePagoFacturaViewSet)
router.register('utils-payment', UtilsPaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('utils-clientes/', UtilsClientesViewSet.as_view()),
    path('utils-cotizaciones/', UtilsCotizacionViewSet.as_view()),
    path('generate-check/', GenerateCheckViewSet.as_view()),
    path('required-documents/', RequiredDocumentsViewSet.as_view()),
    path('comisiones-update/<uuid:proyecto_id>', UpdateComisionesAPIView.as_view())
]
