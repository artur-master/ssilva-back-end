import uuid
from django.db import models


class Cuota(models.Model):
    CuotaID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Amount = models.DecimalField(
        max_digits=30,
        decimal_places=10)
    Date = models.DateTimeField()
    Observacion = models.CharField(null=True,
        blank=True, max_length=300)

    def __str__(self):
        return '%s - %s' % (self.Date, self.Amount)


class PayType(models.Model):
    PayTypeID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class ProductoFinanciero(models.Model):
    ProductoFinancieroID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=20)
    Value = models.DecimalField(
        max_digits=10,
        decimal_places=2)

    def __str__(self):
        return '%s - %s' % (self.Name, self.Value)


class Subsidio(models.Model):
    SubsidioID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Value = models.DecimalField(
        max_digits=10,
        decimal_places=2)
    Ahorro = models.DecimalField(
        max_digits=10,
        decimal_places=2)

    def __str__(self):
        return self.Name


class PreAprobacionCredito(models.Model):
    PreAprobacionCreditoID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    OfertaID = models.ForeignKey(
        'Oferta',
        related_name='oferta_pre_aprobacion_credito',
        on_delete=models.CASCADE)
    InstitucionFinanciera = models.CharField(max_length=100)
    Date = models.DateField(null=True, blank=True)
    Result = models.CharField(
        max_length=100, null=True, blank=True)
    DocumentCredit = models.FileField(
        upload_to="PreAprobacionCredito", null=True, blank=True)
    DocumentPreApprobal = models.FileField(
        upload_to="PreAprobacionCredito", null=True, blank=True)
    Observacion = models.CharField(null=True, max_length=300)
    def __str__(self):
        return '%s - %s' % (self.OfertaID.Folio, self.InstitucionFinanciera)
