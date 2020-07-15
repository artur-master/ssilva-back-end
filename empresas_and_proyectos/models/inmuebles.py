import uuid
from django.db import models
from empresas_and_proyectos.models.edificios import Edificio
from empresas_and_proyectos.models.etapas import Etapa

# Managers


class OrientationManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class TipologiaManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class InmuebleTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class InmuebleStateManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)

# Models


class Orientation(models.Model):
    OrientationID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=10)
    Description = models.TextField(null=True, blank=True)

    objects = OrientationManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class Tipologia(models.Model):
    TipologiaID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=40)
    Description = models.TextField(null=True, blank=True)

    objects = TipologiaManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class InmuebleType(models.Model):
    InmuebleTypeID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=40)
    Description = models.TextField(null=True, blank=True)

    objects = InmuebleTypeManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class InmuebleState(models.Model):
    InmuebleStateID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=40)

    objects = InmuebleStateManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class Inmueble(models.Model):
    InmuebleID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        null=True)
    InmuebleTypeID = models.ForeignKey(
        InmuebleType,
        related_name='tipo_inmueble',
        on_delete=models.CASCADE)
    TipologiaID = models.ForeignKey(
        Tipologia,
        null=True,
        blank=True,
        related_name='tipologia_inmueble',
        on_delete=models.CASCADE)
    EtapaID = models.ForeignKey(
        Etapa,
        related_name='etapa_inmueble',
        on_delete=models.CASCADE)
    EdificioID = models.ForeignKey(
        Edificio,
        null=True,
        blank=True,
        related_name='edificio_inmueble',
        on_delete=models.CASCADE)
    OrientationID = models.ManyToManyField(
        Orientation,
        related_name='orientation_inmueble')
    Number = models.IntegerField()
    Floor = models.IntegerField(
        null=True,
        blank=True)
    BathroomQuantity = models.IntegerField(
        null=True,
        blank=True)
    BedroomsQuantity = models.IntegerField(
        null=True,
        blank=True)
    UtilSquareMeters = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    TerraceSquareMeters = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    LodgeSquareMeters = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    TotalSquareMeters = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    IsNotUsoyGoce = models.BooleanField(default=False)
    Price = models.DecimalField(
        max_digits=10,
        decimal_places=2)
    MaximumDiscount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=100,
        null=True,
        blank=True)
    CotizacionDuration = models.IntegerField()
    InmuebleStateID = models.ForeignKey(
        InmuebleState,
        related_name='estado_inmueble',
        on_delete=models.CASCADE)
    InmuebleRestrict = models.ManyToManyField(
        "self",
        symmetrical=False,
        through='InmuebleInmueble',
        through_fields=(
            'InmuebleAID',
            'InmuebleBID'))
    BluePrint = models.CharField(max_length=100, null=True)
    Up_Print = models.FileField(upload_to="ProyectoDocuments/Inmueble", null=True, blank=True,)

    def __str__(self):
        return '%s - %s, %s,%s' % (self.InmuebleTypeID,
                                   self.Number, self.EdificioID, self.EtapaID)
