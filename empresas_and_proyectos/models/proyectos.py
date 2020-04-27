import uuid
from datetime import datetime

from django.db import models
from django.contrib.postgres.fields import JSONField
from common.models import ContactInfoType, Comuna
from empresas_and_proyectos.models.aseguradoras import Aseguradora
from empresas_and_proyectos.models.etapastate import EtapaState
from empresas_and_proyectos.models.project_documents import ProjectDocument
from users.models import User
from empresas_and_proyectos.models.constructoras import Constructora
from empresas_and_proyectos.models.inmobiliarias import Inmobiliaria
from empresas_and_proyectos.models.instituciones_financieras import InstitucionFinanciera
from empresas_and_proyectos.models.states import (
    PlanMediosState,
    BorradorPromesaState,
    IngresoComisionesState)


def marketing_directory_path(instance, filename):
    return 'ProyectoMarketing/{0}/{1}/{2}'.format(datetime.now().strftime("%Y-%m-%d"), instance.ProyectoID, filename)


def legal_directory_path(instance, filename):
    return 'ProyectoLegal/{0}/{1}/{2}'.format(datetime.now().strftime("%Y-%m-%d"), instance.ProyectoID, filename)


def finance_directory_path(instance, filename):
    return 'ProyectoFinance/{0}/{1}/{2}'.format(datetime.now().strftime("%Y-%m-%d"), instance.ProyectoID, filename)


# Managers
class ProyectosManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class UserProyectoTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class ProyectoApprovalStateManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class ProyectoAseguradoraManager(models.Manager):
    def get_by_natural_key(self, uuid):
        return self.get(ProyectoAseguradoraID=uuid)

# Models


class ProyectoApprovalState(models.Model):
    ProyectoApprovalStateID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=40)

    objects = ProyectoApprovalStateManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class Proyecto(models.Model):
    ProyectoID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    InstitucionFinancieraID = models.ForeignKey(
        InstitucionFinanciera,
        related_name="institucion_financiera_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    Name = models.CharField(max_length=150)
    Arquitecto = models.CharField(max_length=150, null=True, blank=True)
    Symbol = models.CharField(max_length=20, null=True, blank=True)
    Address = models.CharField(max_length=150, null=True, blank=True)
    ContactInfo = models.ManyToManyField(
        ContactInfoType,
        related_name="contacto_proyecto",
        through='ProyectoContactInfo')
    ComunaID = models.ForeignKey(
        Comuna,
        related_name="comuna_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    InmobiliariaID = models.ForeignKey(
        Inmobiliaria,
        related_name="inmobiliaria_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    ConstructoraID = models.ForeignKey(
        Constructora,
        related_name="constructora_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    ProyectoAseguradoraID = models.ForeignKey(
        'ProyectoAseguradora',
        related_name='aseguradora_proyecto',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    ProyectoApprovalState = models.ForeignKey(
        ProyectoApprovalState,
        related_name="estado_aprobacion_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    CotizacionDuration = models.IntegerField(blank=True, null=True)
    GuaranteeAmount = models.IntegerField(null=True, blank=True)
    
    ContadoMontoPromesa = models.IntegerField(null=True, blank=True)
    ContadoMontoCuotas = models.IntegerField(null=True, blank=True)
    ContadoMontoEscrituraContado = models.IntegerField(null=True, blank=True)
    ContadoAhorroPlus = models.IntegerField(null=True, blank=True)
    
    CreditoMontoPromesa = models.IntegerField(null=True, blank=True)
    CreditoMontoCuotas = models.IntegerField(null=True, blank=True)
    CreditoMontoEscrituraContado = models.IntegerField(null=True, blank=True)
    CreditoAhorroPlus = models.IntegerField(null=True, blank=True)

    DiscountMaxPercent = models.DecimalField(        
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    MoreThanOneEtapa = models.BooleanField(default=False)
    PlanMediosState = models.ForeignKey(
        PlanMediosState,
        related_name="estado_plan_medios_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    BorradorPromesaState = models.ForeignKey(
        BorradorPromesaState,
        related_name="estado_borrador_promesa_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    IngresoComisionesState = models.ForeignKey(
        IngresoComisionesState,
        related_name="estado_ingreso_comisiones_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    UserProyecto = models.ManyToManyField(
        User,
        related_name='usuario_proyecto',
        through='UserProyecto',
        through_fields=(
            'ProyectoID',
            'UserID'))
    ProyectoLog = models.ManyToManyField(
        User,
        related_name='bitacora_proyecto',
        through='ProyectoLog')
    EtapaStateID = models.ForeignKey(
        EtapaState,
        related_name="etapastate_proyecto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    EntregaInmediata = models.BooleanField(default=False)
    Documents = models.ManyToManyField(
        ProjectDocument,
        related_name='document_project'
    )

    objects = ProyectosManager()

    #Escritura
    EscrituraProyectoState = models.DecimalField(
        null=True, max_digits=10, decimal_places=2)
    SubmissionDate = models.DateField(
        null=True, blank=True)
    ReceptionDate = models.DateField(
        null=True, blank=True)
    RealEstateLawDate = models.DateField(
        null=True, blank=True)
    RealEstateLawFile = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    PlansConservatorDate = models.DateField(
        null=True, blank=True)
    PlansConservatorFile = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    DeedStartDate = models.DateField(
        null=True, blank=True)
    DeliverDay = models.IntegerField(
        null=True, blank=True)
    StateBankReportDate = models.DateField(
        null=True, blank=True)
    StateBankReportFile = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    StateBankObservations = JSONField(
        default=[], blank=True, null=True)
    StateBankState = models.CharField(
        max_length=200, null=True, blank=True)
    SantanderReportDate = models.DateField(
        null=True, blank=True)
    SantanderReportFile = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    SantanderObservations = JSONField(
        default=[], blank=True, null=True)
    SantanderState = models.CharField(
        max_length=200, null=True, blank=True)
    ChileBankReportDate = models.DateField(
        null=True, blank=True)
    ChileBankReportFile = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    ChileBankObservations = JSONField(
        default=[], blank=True, null=True)
    ChileBankState = models.CharField(
        max_length=200, null=True, blank=True)

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class UserProyectoType(models.Model):
    UserProyectoTypeID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=40)

    objects = UserProyectoTypeManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class ProyectoContactInfo(models.Model):
    ProyectoID = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE)
    ContactInfoTypeID = models.ForeignKey(
        ContactInfoType,
        on_delete=models.CASCADE)
    Value = models.CharField(max_length=60)

    def __str__(self):
        return '%s - %s - %s' % (self.ProyectoID,
                                 self.ContactInfoTypeID, self.Value)


class UserProyecto(models.Model):
    UserID = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    ProyectoID = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE)
    UserProyectoTypeID = models.ForeignKey(
        UserProyectoType,
        on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s - %s' % (self.ProyectoID,
                                 self.UserID, self.UserProyectoTypeID)


class ProyectoAseguradora(models.Model):
    ProyectoAseguradoraID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    AseguradoraID = models.ForeignKey(
        Aseguradora,
        on_delete=models.CASCADE)
    Amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    ExpirationDate = models.DateTimeField(
        null=True,
        blank=True)

    objects = ProyectoAseguradoraManager()

    def __str__(self):
        return '%s' % (self.AseguradoraID)

    def natural_key(self):
        return (self.ProyectoAseguradoraID,)