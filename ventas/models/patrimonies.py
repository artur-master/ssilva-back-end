import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from ventas.models.clientes import Cliente


class Patrimony(models.Model):
    PatrimonyID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    ClienteID = models.ForeignKey(
        Cliente,
        related_name='cliente_patrimony',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    RealState = models.PositiveIntegerField(default=0, null=True, blank=True)
    Vehicle = models.PositiveIntegerField(default=0, null=True, blank=True)
    DownPayment = models.PositiveIntegerField(default=0, null=True, blank=True)
    Other = models.PositiveIntegerField(default=0, null=True, blank=True)
    CreditCard = JSONField(null=True, blank=True)
    CreditoConsumo = JSONField(null=True, blank=True)
    CreditoHipotecario = JSONField(null=True, blank=True)
    PrestamoEmpleador = JSONField(null=True, blank=True)
    CreditoComercio = JSONField(null=True, blank=True)
    DeudaIndirecta = JSONField(null=True, blank=True)
    AnotherCredit = JSONField(null=True, blank=True)
    Deposits = models.FloatField(default=0, null=True, blank=True)
    Rent = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return 'Patrimonio Cliente: %s' % (self.ClienteID)
