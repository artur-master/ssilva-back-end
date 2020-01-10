import uuid
from django.db import models
from users.models import User
from common.models import ContactInfoType, Comuna
from empresas_and_proyectos.models.aseguradoras import Aseguradora
from empresas_and_proyectos.models.instituciones_financieras import InstitucionFinanciera
from empresas_and_proyectos.models.inmobiliarias import Inmobiliaria
from empresas_and_proyectos.models.constructoras import Constructora
from empresas_and_proyectos.models.etapas import EtapaState
from empresas_and_proyectos.models.inmuebles_restrictions import InmuebleInmuebleType
from empresas_and_proyectos.models.proyectos import (
    UserProyectoType,
    Proyecto)
from empresas_and_proyectos.models.inmuebles import (
    InmuebleType,
    InmuebleState,
    Tipologia,
    Orientation)
from empresas_and_proyectos.models.states import (
    PlanMediosState,
    BorradorPromesaState,
    IngresoComisionesState)

# Create your models here.


class CounterHistory(models.Model):
    Count = models.IntegerField(default=1)
    ProyectoID = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.ProyectoID, self.Count)


class HistoricalProyectoAseguradora(models.Model):
    ProyectoAseguradoraID = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    AseguradoraID = models.ForeignKey(Aseguradora, on_delete=models.CASCADE)
    Amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    ExpirationDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s' % (self.AseguradoraID)

    def natural_key(self):
        return (self.ProyectoAseguradoraID,)


class HistoricalProyecto(models.Model):
    HistoricalProyectoID = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    ProyectoID = models.UUIDField()
    Counter = models.IntegerField(default=0)
    Date = models.DateTimeField(auto_now_add=True)
    InstitucionFinancieraID = models.ForeignKey(
        InstitucionFinanciera,
        related_name="historical_institucion_financiera_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    Name = models.CharField(max_length=150)
    Arquitecto = models.CharField(max_length=150, null=True, blank=True)
    Symbol = models.CharField(max_length=20, null=True, blank=True)
    Address = models.CharField(max_length=150, null=True, blank=True)
    ContactInfo = models.ManyToManyField(
        ContactInfoType,
        related_name="historical_contacto_proyecto",
        through='HistoricalProyectoContactInfo')
    ComunaID = models.ForeignKey(
        Comuna,
        related_name="historical_comuna_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    InmobiliariaID = models.ForeignKey(
        Inmobiliaria,
        related_name="historical_inmobiliaria_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    ConstructoraID = models.ForeignKey(
        Constructora,
        related_name="historical_constructora_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    ProyectoAseguradoraID = models.ForeignKey(
        HistoricalProyectoAseguradora,
        related_name='historical_aseguradora_proyecto',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    CotizacionDuration = models.IntegerField(null=True, blank=True)
    GuaranteeAmount = models.IntegerField(null=True, blank=True)
    MoreThanOneEtapa = models.BooleanField(default=False)
    PlanMediosState = models.ForeignKey(
        PlanMediosState,
        related_name="historical_estado_plan_medios_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    BorradorPromesaState = models.ForeignKey(
        BorradorPromesaState,
        related_name="historical_estado_borrador_promesa_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    IngresoComisionesState = models.ForeignKey(
        IngresoComisionesState,
        related_name="historical_estado_ingreso_comisiones_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    UserProyecto = models.ManyToManyField(
        User,
        related_name='historical_usuario_proyecto',
        through='HistoricalUserProyecto',
        through_fields=(
            'ProyectoID',
            'UserID'))

    def __str__(self):
        return self.Name


class HistoricalProyectoContactInfo(models.Model):
    ProyectoID = models.ForeignKey(
        HistoricalProyecto,
        on_delete=models.CASCADE)
    ContactInfoTypeID = models.ForeignKey(
        ContactInfoType, on_delete=models.CASCADE)
    Value = models.CharField(max_length=60)

    def __str__(self):
        return '%s - %s - %s' % (self.ProyectoID,
                                 self.ContactInfoTypeID, self.Value)


class HistoricalUserProyecto(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    ProyectoID = models.ForeignKey(
        HistoricalProyecto,
        on_delete=models.CASCADE)
    UserProyectoTypeID = models.ForeignKey(
        UserProyectoType, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s - %s' % (self.ProyectoID,
                                 self.UserID, self.UserProyectoTypeID)


class HistoricalEtapa(models.Model):
    EtapaID = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=40)
    SalesStartDate = models.DateTimeField(null=True, blank=True)
    EtapaStateID = models.ForeignKey(
        EtapaState,
        related_name="historical_estado_etapa",
        on_delete=models.CASCADE)
    ProyectoID = models.ForeignKey(
        HistoricalProyecto,
        related_name='historical_proyecto_etapa',
        on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class HistoricalEdificio(models.Model):
    EdificioID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=40)
    EtapaID = models.ForeignKey(
        HistoricalEtapa,
        related_name='historical_etapa_edificio',
        on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class HistoricalInmueble(models.Model):
    InmuebleID = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        null=True)
    InmuebleTypeID = models.ForeignKey(
        InmuebleType,
        related_name='historical_tipo_inmueble',
        on_delete=models.CASCADE)
    TipologiaID = models.ForeignKey(
        Tipologia,
        null=True,
        blank=True,
        related_name='historical_tipologia_inmueble',
        on_delete=models.CASCADE)
    EtapaID = models.ForeignKey(
        HistoricalEtapa,
        related_name='historical_etapa_inmueble',
        on_delete=models.CASCADE)
    EdificioID = models.ForeignKey(
        HistoricalEdificio,
        null=True,
        blank=True,
        related_name='historical_edificio_inmueble',
        on_delete=models.CASCADE)
    OrientationID = models.ManyToManyField(
        Orientation, related_name='historical_orientation_inmueble')
    Number = models.IntegerField()
    Floor = models.IntegerField(null=True, blank=True)
    BathroomQuantity = models.IntegerField(null=True, blank=True)
    BedroomsQuantity = models.IntegerField(null=True, blank=True)
    UtilSquareMeters = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    TerraceSquareMeters = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    LodgeSquareMeters = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    TotalSquareMeters = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    IsNotUsoyGoce = models.BooleanField(default=False)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    MaximunDiscount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    CotizacionDuration = models.IntegerField(null=True, blank=True,default=0)
    InmuebleStateID = models.ForeignKey(
        InmuebleState,
        related_name='historical_estado_inmueble',
        on_delete=models.CASCADE)
    InmuebleRestrict = models.ManyToManyField(
        "self",
        symmetrical=False,
        through='HistoricalInmuebleInmueble',
        through_fields=(
            'InmuebleAID',
            'InmuebleBID'))

    def __str__(self):
        return '%s - %s, %s,%s' % (self.InmuebleTypeID,
                                   self.Number, self.EdificioID, self.EtapaID)


class HistoricalInmuebleInmueble(models.Model):
    InmuebleAID = models.ForeignKey(
        HistoricalInmueble,
        related_name='historical_inmueble_inmueble_a',
        on_delete=models.CASCADE)
    InmuebleBID = models.ForeignKey(
        HistoricalInmueble,
        related_name='historical_inmueble_inmueble_b',
        on_delete=models.CASCADE)
    InmuebleInmuebleTypeID = models.ForeignKey(
        InmuebleInmuebleType, on_delete=models.CASCADE)

    def __str__(self):
        return '%s | %s, %s' % (self.InmuebleAID,
                                self.InmuebleBID,
                                self.InmuebleInmuebleTypeID)
