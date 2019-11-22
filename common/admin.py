from django.contrib import admin
from .models import *

# Register your models here.

# Declaracion de modelos que apareceran en el administrador de django


class ComunaAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'ComunaID')
    search_fields = ('Name',)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk')


class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk')


class ContactInfoTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'pk', 'ContactInfoTypeID')


class APIUpdateAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Date', 'pk')


class UFAdmin(admin.ModelAdmin):
    list_display = ('Date', 'Value', 'pk')


# Registro de modelos para que el admin los pueda mostrar
 
admin.site.register(Comuna, ComunaAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(ContactInfoType, ContactInfoTypeAdmin)
admin.site.register(NotificationType)
admin.site.register(Notification)
admin.site.register(APIUpdate, APIUpdateAdmin)
admin.site.register(UF, UFAdmin)
admin.site.register(ConstantNumeric)
