import uuid
from django.db import models

from common import constants
from empresas_and_proyectos.models.inmobiliarias import Inmobiliaria
from empresas_and_proyectos.models.inmuebles import Inmueble
from empresas_and_proyectos.models.proyectos import Proyecto


class Factura(models.Model):
    FacturaID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Number = models.IntegerField(
        null=True,
        blank=True)
    InmobiliariaID = models.ForeignKey(
        Inmobiliaria,
        related_name='inmobiliaria_factura',
        on_delete=models.CASCADE)
    ProyectoID = models.ForeignKey(
        Proyecto,
        related_name='proyecto_factura',
        on_delete=models.CASCADE)
    Value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    Date = models.DateTimeField(auto_now_add=True)
    DateEnvio = models.DateTimeField(
        null=True,
        blank=True)
    DatePayment = models.DateTimeField(
        null=True,
        blank=True)
    FacturaState = models.CharField(max_length=100)
    Folio = models.CharField(max_length=50, null=True, blank=True)
    InmuebleID = models.ManyToManyField(
        Inmueble,
        related_name='inmuebles_factura',
        through='FacturaInmueble')

    def __str__(self):
        return '%s - %s' % (self.ProyectoID.Name, self.FacturaState)


class FacturaInmueble(models.Model):
    FacturaID = models.ForeignKey(
        Factura,
        related_name='factura_factura_inmueble',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    InmuebleID = models.ForeignKey(
        Inmueble,
        related_name='inmueble_factura_inmueble',
        on_delete=models.CASCADE)
    ProyectoID = models.ForeignKey(
        Proyecto,
        related_name='proyecto_factura_inmueble',
        on_delete=models.CASCADE)
    FolioVenta = models.CharField(max_length=50)
    Price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    Comision = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    Tipo = models.CharField(max_length=50)
    State = models.CharField(max_length=50)

    def __str__(self):
        return '%s - %s' % (self.ProyectoID.Name, self.State)


class ComisionInmobiliaria(models.Model):
    ProyectoID = models.ForeignKey(
        Proyecto,
        related_name='proyecto_comision_inmobiliaria',
        on_delete=models.CASCADE)
    PromesaFirmada = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    EscrituraFirmada = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    CierreGestion = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    State = models.CharField(choices=[
        (constants.DocumentState.TO_CONFIRM, 'To Confirm'),
        (constants.DocumentState.CONFIRMED, 'Confirmed'),
        (constants.DocumentState.REJECTED, 'Rejected')
    ], default=constants.DocumentState.TO_CONFIRM, null=False, max_length=50)
    NoExisted = models.BooleanField(default=False)

    def __str__(self):
        return 'Comisiones: %s' % (self.ProyectoID.Name)
