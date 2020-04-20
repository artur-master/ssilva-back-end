import uuid
from django.contrib.postgres.fields import JSONField
from django.db import models

from empresas_and_proyectos.models.proyectos import Proyecto
from users.models import User

class Escritura(models.Model):
    EscrituraID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    ProyectoID = models.ForeignKey(
        Proyecto,
        related_name='proyecto_escritura',
        on_delete=models.CASCADE)
    EscrituraState = models.DecimalField(
        max_digits=10,
        decimal_places=2)
    SubmissionDate = models.DateTimeField(
        null=True, blank=True)
    CarepetaFisicaState = models.BooleanField(
        default=False)
    PromesaInstructions = models.NullBooleanField(
        max_length=3,
        blank=True,
        null=True,
        default=None)
    AgreedDeedDate = models.NullBooleanField(
        max_length=3,
        blank=True,
        null=True,
        default=None)
    DepartmentDeliveryDate = models.NullBooleanField(
        max_length=3,
        blank=True,
        null=True,
        default=None)
    SpecialWithdrawalClause = models.NullBooleanField(
        max_length=3,
        blank=True,
        null=True,
        default=None)       
    ModificationFinesClause = models.NullBooleanField(
        max_length=3,
        blank=True,
        null=True,
        default=None)       
    SpecialCommunication = models.NullBooleanField(
        max_length=3,
        blank=True,
        null=True,
        default=None)
    HasPromotion = models.NullBooleanField(
        max_length=3,
        blank=True, null=True,
        default=None)
    CustomerCheckingAccount = models.FileField(
        upload_to="DocumentVentas",
        null=True,
        blank=True)
    PowersCharacteristics = models.FileField(
        upload_to="DocumentVentas",
        null=True,
        blank=True)
    ReceptionDate = models.DateTimeField(
        null=True, blank=True)
    RealEstateLawDate = models.DateTimeField(
        null=True, blank=True)
    RealEstateLawFile = models.FileField(
        upload_to="DocumentVentas",
        null=True,
        blank=True)
    PlansConservatorDate = models.DateTimeField(
        null=True, blank=True)
    PlansConservatorFile = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    DeedStartDate = models.DateTimeField(
        null=True, blank=True)
    DeliverDay = models.IntegerField(
        null=True, blank=True)
    AprobacionCreditoState = models.NullBooleanField(
        max_length=3,
        blank=True,
        null=True,
        default=None)
    DeclarePhysicalFolderState = models.BooleanField(
        default=False)
        
    MatrixDeed = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    MatrixInstructions = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    PromesaDeed = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    PromesaCoinciden = models.NullBooleanField(
        max_length=3,
        blank=True,
        null=True,
        default=None)

    def __str__(self):
        return '%s - %s' % (self.ProyectoID.Name, self.EscrituraState)

class TitleReports(models.Model):
    EscrituraID = models.ForeignKey(
        Escritura,
        on_delete=models.CASCADE)
    StateBankDate = models.DateTimeField(
        null=True, blank=True)
    StateBankState = models.CharField(
        max_length=200, null=True, blank=True)
    StateBankReport = models.FileField(
        upload_to="DocumentVentas",
        null=True,
        blank=True)
    SantanderDate = models.DateTimeField(
        null=True, blank=True)
    SantanderState = models.CharField(
        max_length=200, null=True, blank=True)
    SantanderReport = models.FileField(
        upload_to="DocumentVentas",
        null=True,
        blank=True)
    ChileBankDate = models.DateTimeField(
        null=True, blank=True)
    ChileBankState = models.CharField(
        max_length=200, null=True, blank=True)
    ChileBankReport = models.FileField(
        upload_to="DocumentVentas",
        null=True,
        blank=True)

    def __str__(self):
        return '%s - %s, %s, %s' % (
            self.EscrituraID,
            self.StateBankDate,
            self.SantanderDate,
            self.ChileBankDate)

class ReportsObservations(models.Model):
    ReportID = models.ForeignKey(
        TitleReports,
        on_delete=models.CASCADE)
    Date = models.DateTimeField(auto_now_add=True)
    Observation = models.CharField(
        max_length=200, null=True, blank=True)
    Class = models.CharField(
        max_length=200, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.ReportID, self.Date)