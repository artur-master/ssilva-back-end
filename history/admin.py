from django.contrib import admin
from .models import *

# Register your models here.

# Modelos a incluir en el admin de django


class HistoricalProyectoAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'HistoricalProyectoID',
                    'ProyectoID')


class HistoricalInmuebleAdmin(admin.ModelAdmin):
    list_display = ('InmuebleTypeID', 'Number', 'EdificioID',
                    'EtapaID', 'pk', 'InmuebleID')


admin.site.register(HistoricalProyectoAseguradora)
admin.site.register(HistoricalProyecto, HistoricalProyectoAdmin)
admin.site.register(HistoricalProyectoContactInfo)
admin.site.register(HistoricalUserProyecto)
admin.site.register(HistoricalEtapa)
admin.site.register(HistoricalEdificio)
admin.site.register(HistoricalInmueble, HistoricalInmuebleAdmin)
admin.site.register(HistoricalInmuebleInmueble)
admin.site.register(CounterHistory)
