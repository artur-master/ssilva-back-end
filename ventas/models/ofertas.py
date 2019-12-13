import uuid
from django.db import models
from empresas_and_proyectos.models.proyectos import Proyecto
from ventas.models.clientes import Cliente
from users.models import User
from ventas.models.empresas_compradoras import EmpresaCompradora
from ventas.models.finding_contact import ContactMethodType
from ventas.models.payment_forms import PayType
from ventas.models.cotizaciones import CotizacionType

class Oferta(models.Model):
    OfertaID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    ProyectoID = models.ForeignKey(
        Proyecto,
        related_name='proyecto_oferta',
        on_delete=models.CASCADE)
    CotizacionTypeID = models.ForeignKey(
        CotizacionType,
        related_name='tipo_cotizacion_oferta',
        on_delete=models.CASCADE,
        null=True,
        blank=True)     
    ClienteID = models.ForeignKey(
        Cliente,
        related_name='cliente_oferta',
        on_delete=models.CASCADE)
    VendedorID = models.ForeignKey(
        User,
        related_name="vendedor_oferta",
        on_delete=models.CASCADE)
    CodeudorID = models.ForeignKey(
        Cliente,
        related_name='codeudor_oferta',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    EmpresaCompradoraID = models.ForeignKey(
        EmpresaCompradora,
        related_name='empresa_compradora_oferta',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    Date = models.DateTimeField(auto_now_add=True)
    Folio = models.CharField(max_length=50)
    OfertaState = models.CharField(max_length=100)
    AprobacionInmobiliariaState = models.CharField(max_length=100)
    PreAprobacionCreditoState = models.CharField(max_length=100)
    RecepcionGarantiaState = models.CharField(max_length=100)
    ContactMethodTypeID = models.ForeignKey(
        ContactMethodType,
        related_name='medio_contacto_oferta',
        on_delete=models.CASCADE)
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
    PayTypeID = models.ForeignKey(
        PayType,
        related_name='tipo_pago_oferta',
        on_delete=models.CASCADE)
    DateFirmaPromesa = models.DateTimeField(
        null=True,
        blank=True)
    ValueProductoFinanciero = models.IntegerField(
        null=True,
        blank=True)
    IsApproveInmobiliaria = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.ProyectoID.Name, self.OfertaState)

