from django.conf.urls import include
from django.urls import path
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
from ventas.views.desistimiento import (
    RegisterDesistimientoViewSet,
    UploadConfeccionDesistimientoViewSet,
    RegisterRefundViewSet)
from ventas.views.facturas import (
    ComisionInmobiliariaViewSet,
    UpdateComisionesAPIView,
    FacturaInmuebleViewSet,
    FacturaViewSet,
    DownloadFacturaViewSet,
    DownloadNotaCreditoViewSet, RegisterSendFacturaViewSet, RegisterDatePagoFacturaViewSet, RegisterNoteCreditViewSet)
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
from ventas.views.promesas import (
    PromesaViewSet,
    UploadConfeccionPromesaViewSet,
    UploadFirmaDocumentViewSet,
    ApproveMaquetaPromesaViewSet,
    ApproveControlPromesaViewSet,
    RegisterSendPromesaToInmobiliariaViewSet,
    GenerateFacturaViewSet,
    RegisterSignatureInmobiliariaViewSet,
    LegalizePromesaViewSet,
    SendCopiesViewSet,
    NegociacionPromesaViewSet,
    SendNegociacionPromesaViewSet,
    ControlNegociacionPromesaViewSet, SendPromesaToClientViewSet)
from ventas.views.reservas import (
    ReservaViewSet,
    CancelReservaViewSet,
    SendControlReservaViewSet,
    ApproveControlReservaViewSet,
    UploadDocumentsReservaViewSet,
    DownloadPreApprobationViewSet)
from ventas.views.utils import (
    UtilsClientesViewSet,
    UtilsCotizacionViewSet,
    GenerateCheckViewSet,
    RequiredDocumentsViewSet, UtilsPaymentViewSet)
from ventas.views.ventas_logs import (
    VentaLogViewSet,
    VentaLogClienteViewSet,
    VentaLogVendedorViewSet,
    VentaLogUserViewSet,
    UserSummaryViewSet)

from ventas.views.escrituras import (
    EscrituraViewSet)
from ventas.views.dashboard import (
    PendingActionsViewSet,
    AllLogsViewSet,
    AllUserViewSet)

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
router.register('pre-approbation-download', DownloadPreApprobationViewSet)

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
    'promesas-upload-confeccion-promesa',
    UploadConfeccionPromesaViewSet)

router.register(
    'promesas-approve-maqueta',
    ApproveMaquetaPromesaViewSet)
router.register(
    'promesas-upload-firma-document',
    UploadFirmaDocumentViewSet)
router.register(
    'promesas-approve-control',
    ApproveControlPromesaViewSet)
router.register(
    'promesas-register-send',
    RegisterSendPromesaToInmobiliariaViewSet)
router.register(
    'promesas-generate-factura',
    GenerateFacturaViewSet)
router.register(
    'promesas-register-signature',
    RegisterSignatureInmobiliariaViewSet)
router.register(
    'promesas-legalize',
    LegalizePromesaViewSet)
router.register(
    'promesas-send-copies',
    SendCopiesViewSet)
router.register(
    'promesas-send-negociacion-to-jp',
    NegociacionPromesaViewSet)
router.register(
    'promesas-send-negociacion-to-in',
    SendNegociacionPromesaViewSet)
router.register(
    'promesas-control-negociacion',
    ControlNegociacionPromesaViewSet)

router.register(
    'promesas-register-desistimiento',
    RegisterDesistimientoViewSet)
router.register(
    'promesas-upload-confeccion-desistimiento',
    UploadConfeccionDesistimientoViewSet)
router.register(
    'promesas-refund',
    RegisterRefundViewSet)
router.register(
    'promesas-send-to-cliente',
    SendPromesaToClientViewSet)

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
router.register('facturas-register-nota-credito', RegisterNoteCreditViewSet)

router.register('utils-payment', UtilsPaymentViewSet)

router.register('dashboard-pending-actions', PendingActionsViewSet)
router.register('all-users', AllUserViewSet)
router.register('all-logs-dashboard', AllLogsViewSet)

router.register('escritura', EscrituraViewSet)

router.register('user-summary', UserSummaryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('utils-clientes/', UtilsClientesViewSet.as_view()),
    path('utils-cotizaciones/', UtilsCotizacionViewSet.as_view()),
    path('generate-check/', GenerateCheckViewSet.as_view()),
    path('required-documents/', RequiredDocumentsViewSet.as_view()),
    path('comisiones-update/<uuid:proyecto_id>', UpdateComisionesAPIView.as_view())
]
