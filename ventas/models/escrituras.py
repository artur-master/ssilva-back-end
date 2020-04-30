import uuid
from django.contrib.postgres.fields import JSONField
from django.db import models

from empresas_and_proyectos.models.proyectos import Proyecto
from ventas.models.promesas import Promesa
from users.models import User


class Escritura(models.Model):
    EscrituraID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    ProyectoID = models.ForeignKey(
        Proyecto,
        related_name='proyecto_escritura',
        null=True,
        on_delete=models.CASCADE)
    PromesaID = models.ForeignKey(
        Promesa,
        related_name='promesa_escritura',
        on_delete=models.CASCADE)
    EscrituraState = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2)
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
    TasacionStateBank = models.FileField(
        upload_to="DocumentVentas",
        null=True,
        blank=True)
    TasacionSantander = models.FileField(
        upload_to="DocumentVentas",
        null=True,
        blank=True)
    TasacionChileBank = models.FileField(
        upload_to="DocumentVentas",
        null=True,
        blank=True)
    RevisionStateBank = models.FileField(
        upload_to="DocumentVentas",
        null=True,
        blank=True)
    RevisionConfirmoStateBank = models.BooleanField(
        default=False)
    RevisionSantander = models.FileField(
        upload_to="DocumentVentas",
        null=True,
        blank=True)
    RevisionConfirmoSantander = models.BooleanField(
        default=False)
    RevisionChileBank = models.FileField(
        upload_to="DocumentVentas",
        null=True,
        blank=True)        
    RevisionConfirmoChileBank = models.BooleanField(
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
        blank=True,
        null=True,
        default=None)
    NoticeToClientDate = models.DateField(
        null=True, blank=True)
    BalanceFeeUF = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2)
    BalanceFund = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2)
    SignDate = models.DateTimeField(
        null=True, blank=True)
    PaymentMethodBalance = models.IntegerField(
        blank=True, null=True)
    ChequeNumber = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2)
    Valor = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2)
    FetchaPago = models.DateTimeField(
        null=True, blank=True)
    FetchaFirma = models.DateTimeField(
        null=True, blank=True)
    InstructionObservacion = models.CharField(
        max_length=200, null=True, blank=True)
    RepertoireNumber = models.IntegerField(
        blank=True, null=True)
    StartDate = models.DateTimeField(
        null=True, blank=True)
    RealEstateBilling = models.BooleanField(
        default=False)
    InvoiceFile = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    RealEstateSign = models.BooleanField(
        default=False)
    RealEstateSignDate = models.DateTimeField(
        null=True, blank=True)
    SignNotary = models.BooleanField(
        default=False)
    SignNotaryDate = models.DateTimeField(
        null=True, blank=True)
    SignDeedCompensation = models.BooleanField(
        default=False)
    SignDeedCompensationDate = models.DateTimeField(
        null=True, blank=True)
    SignSettelment = models.BooleanField(
        default=False)
    SignSettelmentDate = models.DateTimeField(
        null=True, blank=True)
    SignPay = models.BooleanField(
        default=False)
    SignPayDate = models.DateTimeField(
        null=True, blank=True)
    MortgageLift = models.BooleanField(
        default=False)
    MortgageLiftDate = models.DateTimeField(
        null=True, blank=True)
    RealEstateConservator = models.BooleanField(
        default=False)
    RealEstateConservatorFile = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    SendCopiesToClient = models.BooleanField(
        default=False)
    SendCopiesToClientDate = models.DateTimeField(
        null=True, blank=True)
    SendCopiesToIN = models.BooleanField(
        default=False)
    SendCopiesToINDate = models.DateTimeField(
        null=True, blank=True)
    ProofDeed = models.BooleanField(
        default=False)
    ProofDeedDate = models.DateTimeField(
        null=True, blank=True)
    SubsidyState = models.NullBooleanField(
        blank=True,
        null=True,
        default=None)
    PaymentSubsidy = models.BooleanField(
        default=False)
    PaymentSubsidyFile = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    PaymentSavingIN = models.BooleanField(
        default=False)
    PaymentSavingINFile = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    INPaymentPending = models.BooleanField(
        default=False)
    INPaymentPendingFile = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    GuaranteeToClient = models.BooleanField(
        default=False)
    GuaranteeToClientDate = models.DateTimeField(
        null=True, blank=True)
    DeliveryProperty = models.BooleanField(
        default=False)
    DeliveryPropertyDate = models.DateTimeField(
        null=True, blank=True)
    GPLoginRegistration = models.BooleanField(
        default=False)
    GPLoginRegistrationFile = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)    
    DeclarePhysicalFolderState = models.BooleanField(
        blank=True, default=False)

    def __str__(self):
        return '%s - %s' % (self.ProyectoID.Name, self.PromesaID.Folio)

class AprobacionCredito(models.Model):
    AprobacionCreditoID=models.UUIDField(
        unique=True, default=uuid.uuid4,
        editable=False)
    EscrituraID = models.ForeignKey(
        Escritura,
        on_delete=models.CASCADE)
    FormalCredit = models.BooleanField(
        blank=True, default=False)
    BankName = models.CharField(
        max_length=200, null=True, blank=True)
    ExecutiveName = models.CharField(
        max_length=200, null=True, blank=True)
    ExecutiveEmail = models.EmailField(
        max_length=60, null=True, 
        blank=True, unique=True, 
        error_messages={'unique': 'Email ingresado ya existe en el sistema'})
    ClientPersonalHealthStatement= models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    ClientApprovementLetter = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    AcFinancialInstitution = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    AcObservations = JSONField(
        default=[],
        blank=True,  null=True)
    AprobacionCreditoState = models.NullBooleanField(
        blank=True, null=True,
        default=None)

    def __str__(self):
        return '%s-%s' % (self.EscrituraID, self.AprobacionCreditoID)