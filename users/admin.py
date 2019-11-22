from django.contrib import admin
from .models import *

# Register your models here.


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('Name', 'PermissionID', 'pk')


class RoleAdmin(admin.ModelAdmin):
    list_display = ('Name', 'RoleID', 'pk')


class UserAdmin(admin.ModelAdmin):
    list_display = ('Name', 'LastNames', 'Rut', 'pk', 'UserID')


admin.site.register(Permission, PermissionAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(User, UserAdmin)
