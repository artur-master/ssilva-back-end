from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from empresas_and_proyectos.views.aseguradoras import AseguradoraViewSet
from empresas_and_proyectos.views.inmobiliarias import InmobiliariaViewSet
from empresas_and_proyectos.views.constructoras import ConstructoraViewSet
from empresas_and_proyectos.views.etapas import (
    EtapaViewSet,
    CreateEtapaViewSet,
    CreateMassiveEtapaViewSet,
    EtapaStateViewSet,
    CreateEtapaSingleViewSet)
from empresas_and_proyectos.views.inmuebles import (
    InmuebleViewSet,
    InmuebleTypeViewSet,
    TipologiaViewSet,
    OrientationViewSet,
    InmuebleStateViewSet,
    UpdateInmueblesViewSet)
from empresas_and_proyectos.views.inmuebles_restrictions import (
    InmuebleInmuebleTypeViewSet,
    InmuebleInmuebleRestrictionViewSet)
from empresas_and_proyectos.views.instituciones_financieras import (
    InstitucionFinancieraViewSet)
from empresas_and_proyectos.views.proyectos import (
    ProyectoViewSet,
    UserProyectoTypeViewSet,
    ApproveCreateProyectoLegalViewSet,
    ApproveCreateProyectoGerenciaViewSet,
    AddBorradorPromesaViewSet,
    CreateNotificationLegalUsersViewSet,
    CreateNotificationGerenciaUsersViewSet)
from empresas_and_proyectos.views.proyectos_logs import (
    ProyectoLogViewSet,
    ProyectoLogTypeViewSet)

router = DefaultRouter()

router.register('aseguradoras', AseguradoraViewSet)
router.register('instituciones-financieras', InstitucionFinancieraViewSet)
router.register('inmuebles', InmuebleViewSet)
router.register('inmuebles-types', InmuebleTypeViewSet)
router.register('inmuebles-tipologias', TipologiaViewSet)
router.register('inmuebles-orientations', OrientationViewSet)
router.register('inmuebles-states', InmuebleStateViewSet)
router.register('inmuebles-restriction-types', InmuebleInmuebleTypeViewSet)
router.register('inmuebles-restrictions', InmuebleInmuebleRestrictionViewSet)
router.register('proyectos', ProyectoViewSet)
router.register('proyectos-users-types', UserProyectoTypeViewSet)
router.register('proyectos-approve-legal', ApproveCreateProyectoLegalViewSet)
router.register('proyectos-approve-gerencia', ApproveCreateProyectoGerenciaViewSet)
router.register('proyectos-add-borrador', AddBorradorPromesaViewSet)
router.register('proyectos-etapas', EtapaViewSet)
router.register('proyectos-etapas-inmuebles', CreateEtapaViewSet)
router.register('proyectos-etapas-massive', CreateMassiveEtapaViewSet)
router.register('proyectos-etapas-states', EtapaStateViewSet)
router.register('proyectos-etapas-single', CreateEtapaSingleViewSet)
router.register('proyectos-logs', ProyectoLogViewSet, base_name='proyectos-logs')
router.register('proyectos-logs-types', ProyectoLogTypeViewSet)
router.register('inmobiliarias', InmobiliariaViewSet, base_name='inmobiliarias')
router.register('constructoras', ConstructoraViewSet, base_name='constructoras')
router.register('notifications-legal', CreateNotificationLegalUsersViewSet)
router.register('notifications-gerencia', CreateNotificationGerenciaUsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('inmuebles-edita/', UpdateInmueblesViewSet.as_view())
]
