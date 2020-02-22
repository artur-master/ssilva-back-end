import uuid
from django.contrib.postgres.fields import JSONField
from django.db import models

from empresas_and_proyectos.models.inmuebles import Inmueble
from empresas_and_proyectos.models.proyectos import Proyecto
from users.models import User
from ventas.models.clientes import Cliente
from ventas.models.conditions import Condition
from ventas.models.cotizaciones import CotizacionType
from ventas.models.payment_forms import PayType


class Promesa(models.Model):
    PromesaID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    ProyectoID = models.ForeignKey(
        Proyecto,
        related_name='proyecto_promesa',
        on_delete=models.CASCADE)
    CotizacionTypeID = models.ForeignKey(
        CotizacionType,
        related_name='tipo_cotizacion_promesa',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    ClienteID = models.ForeignKey(
        Cliente,
        related_name='cliente_promesa',
        on_delete=models.CASCADE)
    VendedorID = models.ForeignKey(
        User,
        related_name="vendedor_promesa",
        on_delete=models.CASCADE)
    CodeudorID = models.ForeignKey(
        Cliente,
        related_name='codeudor_promesa',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    InmuebleID = models.ManyToManyField(
        Inmueble,
        related_name='inmuebles_promesa',
        through='PromesaInmueble')
    Date = models.DateTimeField(auto_now_add=True)
    Folio = models.CharField(max_length=50)
    PromesaState = models.CharField(max_length=200)
    AprobacionInmobiliaria = JSONField(
        default=dict,
        blank=True,
        null=True)
    PromesaDesistimientoState = models.CharField(max_length=200, null=True, blank=True)
    PromesaResciliacionState = models.CharField(max_length=200, null=True, blank=True)
    PromesaResolucionState = models.CharField(max_length=200, null=True, blank=True)
    PromesaModificacionState = models.CharField(max_length=200, null=True, blank=True)

    DocumentPromesa = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)

    DocumentPromesaFirma = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentChequesFirma = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentPlantaFirma = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)

    DocumentFirmaComprador = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)

    DocumentResciliacion = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentResciliacionFirma = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentResolucion = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)

    DateEnvioPromesa = models.DateTimeField(
        null=True,
        blank=True)
    DateRegresoPromesa = models.DateTimeField(
        null=True,
        blank=True)
    DateLegalizacionPromesa = models.DateTimeField(
        null=True,
        blank=True)
    DateEnvioCopias = models.DateTimeField(
        null=True,
        blank=True)
    PaymentFirmaPromesa = models.DecimalField(
        max_digits=10,
        decimal_places=2)
    PaymentFirmaEscritura = models.DecimalField(
        max_digits=10,
        decimal_places=2)
    PaymentInstitucionFinanciera = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    AhorroPlus = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    IsOfficial = models.BooleanField(
        default=True
    )
    PayTypeID = models.ForeignKey(
        PayType,
        related_name='tipo_pago_promesa',
        on_delete=models.CASCADE)
    PromesaModified = models.ForeignKey(
        'self',
        related_name='promesa_modificada',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    FechaFirmaDeEscritura = models.DateTimeField(
        null=True,
        blank=True)
    FechaEntregaDeInmueble = models.DateTimeField(
        null=True,
        blank=True)
    DateEnvioPromesaToCliente = models.DateTimeField(
        null=True,
        blank=True)
    DesistimientoEspecial = models.CharField(max_length=255, null=True, blank=True)
    ModificacionEnLaClausula = models.CharField(max_length=255, null=True, blank=True)
    MetodoComunicacionEscrituracion = models.CharField(max_length=255, null=True, blank=True)
    DocumentPaymentForm = models.FileField(upload_to="DocumentVentas", null=True, blank=True)
    DatePayment = models.DateTimeField(
        null=True,
        blank=True)

    def __str__(self):
        return '%s - %s' % (self.ProyectoID.Name, self.PromesaState)


class PromesaInmueble(models.Model):
    PromesaID = models.ForeignKey(
        Promesa,
        on_delete=models.CASCADE)
    InmuebleID = models.ForeignKey(
        Inmueble,
        on_delete=models.CASCADE)
    Discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)

    def __str__(self):
        return '%s - %s' % (self.PromesaID, self.InmuebleID)
