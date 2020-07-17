import uuid
from django.db import models
from empresas_and_proyectos.models.proyectos import Proyecto
from empresas_and_proyectos.models.inmuebles import Inmueble

from ventas.models.clientes import Cliente
from users.models import User
from ventas.models.finding_contact import ContactMethodType
from ventas.models.payment_forms import Cuota, PayType

class CotizacionType(models.Model):
    CotizacionTypeID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name

class CotizacionState(models.Model):
    CotizacionStateID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class Cotizacion(models.Model):
    CotizacionID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    ProyectoID = models.ForeignKey(
        Proyecto,
        related_name='proyecto_cotizacion',
        on_delete=models.CASCADE)
    ClienteID = models.ForeignKey(
        Cliente,
        related_name='cliente_cotizacion',
        on_delete=models.CASCADE)
    CotizadorID = models.ForeignKey(
        User,
        related_name="cotizador_cotizacion",
        on_delete=models.CASCADE)
    CuotaID = models.ManyToManyField(
        Cuota,
        related_name='cuotas_cotizacion')
    InmuebleID = models.ManyToManyField(
        Inmueble,
        related_name='inmuebles_cotizacion',
        through='CotizacionInmueble')
    Date = models.DateTimeField(auto_now_add=True)
    Folio = models.CharField(max_length=50)
    CotizacionStateID = models.ForeignKey(
        CotizacionState,
        related_name='estado_cotizacion',
        on_delete=models.CASCADE)
    CotizacionTypeID = models.ForeignKey(
        CotizacionType,
        related_name='tipo_cotizacion',
        on_delete=models.CASCADE)
    ContactMethodTypeID = models.ForeignKey(
        ContactMethodType,
        related_name='medio_contacto_cotizacion',
        on_delete=models.CASCADE)
    IsNotInvestment = models.NullBooleanField(default=False)
    DateFirmaPromesa = models.DateTimeField(
        null=True,
        blank=True)
    PaymentFirmaPromesa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    PaymentFirmaEscritura = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
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
    Subsidio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)  
    Libreta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    InstitucionFinancieraID = models.UUIDField(
        editable=True,
        blank=True,
        null=True)
    Vendedor = models.ForeignKey(
        User,
        related_name="vendedor_cotizacion",
        on_delete=models.CASCADE,
        null=True)
    PayType = models.ForeignKey(
        PayType,
        related_name="paytype_cotizacion",
        on_delete=models.CASCADE,
        null=True)

    def __str__(self):
        return '%s - %s' % (self.ProyectoID, self.CotizacionTypeID)


class CotizacionInmueble(models.Model):
    CotizacionID = models.ForeignKey(
        Cotizacion,
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
        return '%s - %s' % (self.CotizacionID, self.InmuebleID)
