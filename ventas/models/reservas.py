import uuid
from django.db import models
from empresas_and_proyectos.models.proyectos import Proyecto
from empresas_and_proyectos.models.inmuebles import Inmueble
from ventas.models.clientes import Cliente
from ventas.models.conditions import Condition
from users.models import User
from ventas.models.empresas_compradoras import EmpresaCompradora
from ventas.models.finding_contact import ContactMethodType
from ventas.models.payment_forms import Cuota, PayType
from ventas.models.cotizaciones import CotizacionType



class ReservaState(models.Model):
    ReservaStateID = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=40)

    def __str__(self):
        return self.Name


class Reserva(models.Model):
    ReservaID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    ProyectoID = models.ForeignKey(
        Proyecto,
        related_name='proyecto_reserva',
        on_delete=models.CASCADE)
    CotizacionTypeID = models.ForeignKey(
        CotizacionType,
        related_name='tipo_cotizacion_reserva',
        on_delete=models.CASCADE,
        null=True,
        blank=True)    
    ClienteID = models.ForeignKey(
        Cliente,
        related_name='cliente_reserva',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    VendedorID = models.ForeignKey(
        User,
        related_name="vendedor_reserva",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    CuotaID = models.ManyToManyField(
        Cuota,
        related_name='cuota_reserva',
        null=True,
        blank=True
    )
    InmuebleID = models.ManyToManyField(
        Inmueble,
        related_name='inmuebles_reserva',
        through='ReservaInmueble',
        null=True,
        blank=True
    )
    Date = models.DateTimeField(auto_now_add=True)
    Folio = models.CharField(
        max_length=50,
        null=True,
        blank=True)
    CodeudorID = models.ForeignKey(
        Cliente,
        related_name='codeudor_reserva',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    EmpresaCompradoraID = models.ForeignKey(
        EmpresaCompradora,
        related_name='empresa_compradora_reserva',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    ReservaStateID = models.ForeignKey(
        ReservaState,
        related_name='estado_reserva',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    ConditionID = models.ManyToManyField(
        Condition,
        related_name='condition_reserva',
        null=True,
        blank=True)
    ContactMethodTypeID = models.ForeignKey(
        ContactMethodType,
        related_name='medio_contacto_reserva',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    IsNotInvestment = models.NullBooleanField(default=False)
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
    PayTypeID = models.ForeignKey(
        PayType,
        related_name='tipo_pago_reserva',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    DateFirmaPromesa = models.DateTimeField(
        null=True,
        blank=True)
    ValueProductoFinanciero = models.IntegerField(
        null=True,
        blank=True)

    def __str__(self):
        return '%s - %s' % (self.ProyectoID.Name, self.ReservaStateID.Name)


class ReservaInmueble(models.Model):
    ReservaID = models.ForeignKey(
        Reserva,
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
        return '%s - %s' % (self.ReservaID, self.InmuebleID)
