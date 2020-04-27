import uuid
from django.db import models
from empresas_and_proyectos.models.proyectos import Proyecto
from ventas.models.clientes import Cliente
from users.models import User


class VentaLogType(models.Model):
    VentaLogTypeID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=60)
    MaximunDays = models.IntegerField(default=0)

    def __str__(self):
        return self.Name


class VentaLog(models.Model):
    VentaLogID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    VentaID = models.UUIDField(editable=True)
    Folio = models.CharField(max_length=50, default="",
        null=True,
        blank=True)
    UserID = models.ForeignKey(
        User,
        related_name='vendedor_historial_venta',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    ClienteID = models.ForeignKey(
        Cliente,
        related_name='cliente_historial_venta',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    ProyectoID = models.ForeignKey(
        Proyecto,
        related_name='proyecto_historial_venta',
        on_delete=models.CASCADE)
    VentaLogTypeID = models.ForeignKey(
        VentaLogType,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    Comment = models.TextField(
        null=True,
        blank=True)
    Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.VentaLogTypeID.Name, self.UserID)


class UserSummary(models.Model):
    Nombre = models.TextField(blank=True, null=True)
    UserId = models.IntegerField(blank=True, null=True)
    Tipo = models.TextField(blank=True, null=True)
    UltimaActividad = models.TextField(blank=True, null=True)
    Pendientes = models.TextField(blank=True, null=True)
    TotalUFMes = models.IntegerField(blank=True, null=True)
    TotalUFAno = models.IntegerField(blank=True, null=True)
    ProyectosAsignados = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'ventas_user_summary'