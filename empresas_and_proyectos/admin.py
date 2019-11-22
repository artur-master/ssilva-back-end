from django.contrib import admin
from empresas_and_proyectos.models.aseguradoras import Aseguradora
from empresas_and_proyectos.models.constructoras import Constructora
from empresas_and_proyectos.models.instituciones_financieras import InstitucionFinanciera
from empresas_and_proyectos.models.edificios import Edificio
from empresas_and_proyectos.models.etapas import (
    Etapa,
    EtapaState)
from empresas_and_proyectos.models.inmobiliarias import (
    Inmobiliaria,
    UserInmobiliariaType,
    UserInmobiliaria,
    InmobiliariaContactInfo)
from empresas_and_proyectos.models.inmuebles import (
    Orientation,
    InmuebleType,
    Tipologia,
    InmuebleState,
    Inmueble)
from empresas_and_proyectos.models.inmuebles_restrictions import (
    InmuebleInmuebleType,
    InmuebleInmueble)
from empresas_and_proyectos.models.proyectos import (
    ProyectoApprovalState,
    Proyecto,
    ProyectoAseguradora,
    ProyectoContactInfo,
    UserProyectoType,
    UserProyecto)
from empresas_and_proyectos.models.proyectos_logs import (
    ProyectoLogType,
    ProyectoLog)
from empresas_and_proyectos.models.states import (
    PlanMediosState,
    BorradorPromesaState,
    IngresoComisionesState)


# Modelos a incluir en el admin de django

class InmobiliariaAdmin(admin.ModelAdmin):
    list_display = ('RazonSocial', 'pk', 'InmobiliariaID')


class ConstructoraAdmin(admin.ModelAdmin):
    list_display = ('RazonSocial', 'pk', 'ConstructoraID')


class InstitucionFinancieraAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'InstitucionFinancieraID')


class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'ProyectoID')


class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('InmuebleTypeID', 'Number', 'EdificioID',
                    'EtapaID', 'pk', 'InmuebleID')
    search_fields = ('InmuebleTypeID__Name',)


class ProyectoApprovalStateAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'ProyectoApprovalStateID')


class PlanMediosStateAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'PlanMediosStateID')


class BorradorPromesaStateAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'BorradorPromesaStateID')


class IngresoComisionesStateAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'IngresoComisionesStateID')


class InmuebleTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'InmuebleTypeID')


class InmuebleStateAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'InmuebleStateID')


class InmuebleInmuebleTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'InmuebleInmuebleTypeID')


class TipologiaAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'TipologiaID')


class OrientationAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'OrientationID')


class AseguradoraAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'AseguradoraID')


class UserProyectoTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'UserProyectoTypeID')


class UserInmobiliariaTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'UserInmobiliariaTypeID')


class ProyectoLogTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'MaximunDays',
                    'ProyectoLogTypeID')


class EtapaStateAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'EtapaStateID')


class EtapaAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'EtapaID')


admin.site.register(Inmobiliaria, InmobiliariaAdmin)
admin.site.register(Constructora, ConstructoraAdmin)
admin.site.register(Aseguradora, AseguradoraAdmin)
admin.site.register(InstitucionFinanciera, InstitucionFinancieraAdmin)
admin.site.register(ProyectoApprovalState, ProyectoApprovalStateAdmin)
admin.site.register(PlanMediosState, PlanMediosStateAdmin)
admin.site.register(BorradorPromesaState, BorradorPromesaStateAdmin)
admin.site.register(IngresoComisionesState, IngresoComisionesStateAdmin)
admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(ProyectoAseguradora)
admin.site.register(ProyectoContactInfo)
admin.site.register(UserProyectoType, UserProyectoTypeAdmin)
admin.site.register(UserProyecto)
admin.site.register(ProyectoLogType, ProyectoLogTypeAdmin)
admin.site.register(ProyectoLog)
admin.site.register(UserInmobiliariaType, UserInmobiliariaTypeAdmin)
admin.site.register(UserInmobiliaria)
admin.site.register(InmobiliariaContactInfo)
admin.site.register(Etapa, EtapaAdmin)
admin.site.register(EtapaState, EtapaStateAdmin)
admin.site.register(Edificio)
admin.site.register(Orientation, OrientationAdmin)
admin.site.register(InmuebleType, InmuebleTypeAdmin)
admin.site.register(Tipologia, TipologiaAdmin)
admin.site.register(InmuebleState, InmuebleStateAdmin)
admin.site.register(InmuebleInmuebleType, InmuebleInmuebleTypeAdmin)
admin.site.register(Inmueble, InmuebleAdmin)
admin.site.register(InmuebleInmueble)
