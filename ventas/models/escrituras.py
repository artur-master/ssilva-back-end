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
    Date = models.DateTimeField(
        auto_now_add=True, null=True)
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
    NoticeToClientDate = models.DateField(
        null=True, blank=True)
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
    PromocionDeed = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    PromesaCoinciden = models.BooleanField(
        blank=True, default=True)
    NoticeToClientSignDate = models.DateField(
        null=True, blank=True)
    BalanceFeeUF = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2)
    BalanceFund = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2)
    SignDateEscritura = models.DateTimeField(
        null=True, blank=True)
    SignDatePagare = models.DateTimeField(
        null=True, blank=True)
    SignDateCompensacion = models.DateTimeField(
        null=True, blank=True)
    PaymentMethodBalance = models.IntegerField(
        blank=True, default=0)
    ChequeNumber = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2)
    ChequeFile = models.FileField(
        upload_to="DocumentVentas",
        null=True,
        blank=True)
    Valor = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2)
    FetchaPago = models.DateTimeField(
        null=True, blank=True)
    ProofDeposite = models.FileField(
        upload_to="DocumentVentas",
        null=True,
        blank=True)
    InstructionObservacion = models.CharField(
        max_length=200, null=True, blank=True)
    RepertoireNumber = models.CharField(
        max_length=200, blank=True, null=True)
    StartDate = models.DateTimeField(
        null=True, blank=True)
    RealEstateBilling = models.BooleanField(
        default=False)
    InvoiceFile = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    SendRealEstateSign = models.BooleanField(
        default=False)
    SendRealEstateSignDate = models.DateTimeField(
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
    IngresoAlzamiento = models.BooleanField(
        default=False)
    IngresoAlzamientoDate = models.DateTimeField(
        null=True, blank=True)
    SalidaAlzamiento = models.BooleanField(
        default=False)
    SalidaAlzamientoDate = models.DateTimeField(
        null=True, blank=True)
    EnteranceFISign = models.BooleanField(
        default=False)
    EnteranceFISignDate = models.DateTimeField(
        null=True, blank=True)
    ExitFISign = models.BooleanField(
        default=False)
    ExitFISignDate = models.DateTimeField(
        null=True, blank=True)
    IngresoCierreCopias = models.BooleanField(
        default=False)
    IngresoCierreCopiasDate = models.DateTimeField(
        null=True, blank=True)
    SalidaCierreCopias = models.BooleanField(
        default=False)
    SalidaCierreCopiasDate = models.DateTimeField(
        null=True, blank=True)
    CompensationSettlement = models.BooleanField(
        default=False)
    CompensationSettlementDate = models.DateTimeField(
        null=True, blank=True)
    CompensationRealEstate = models.BooleanField(
        default=False)
    CompensationRealEstateDate = models.DateTimeField(
        null=True, blank=True)
    RealEstateConservator = models.BooleanField(
        default=False)
    RealEstateConservatorDate = models.DateTimeField(
        null=True, blank=True)    
    Cover = models.BooleanField(
        default=False)
    CoverDate = models.DateTimeField(
        null=True, blank=True)    
    SendCopiesToClient = models.BooleanField(
        default=False)
    SendCopiesToClientDate = models.DateTimeField(
        null=True, blank=True)
    SendCopiesToIN = models.BooleanField(
        default=False)
    SendCopiesToINFile = models.FileField(
        upload_to="DocumentVentas",
        null=True, blank=True)
    ProofPaymentSettlement = models.BooleanField(
        default=False)
    ProofPaymentSettlementFile = models.FileField(
        upload_to="DocumentVentas",
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
    Retirement = models.BooleanField(
        default=False)
    RetirementDate = models.DateTimeField(
        null=True, blank=True)
    Subscription = models.BooleanField(
        default=False)
    SubscriptionDate = models.DateTimeField(
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
    Notaria_VII_I_Date = models.DateTimeField(
        null=True, blank=True)
    Notaria_VII_II_Date = models.DateTimeField(
        null=True, blank=True)
    Notaria_VII_III_Date = models.DateTimeField(
        null=True, blank=True)
    Notaria_VII_IV_Date = models.DateTimeField(
        null=True, blank=True)
    Notaria_VII_V_Date = models.DateTimeField(
        null=True, blank=True)
    Notaria_VIII_I_Date = models.DateTimeField(
        null=True, blank=True)
    Notaria_VIII_II_Date = models.DateTimeField(
        null=True, blank=True)
    Notaria_VIII_III_Date = models.DateTimeField(
        null=True, blank=True)
    Notaria_VIII_IV_Date = models.DateTimeField(
        null=True, blank=True)
    Notaria_VIII_V_Date = models.DateTimeField(
        null=True, blank=True)
    Notaria_VIII_VI_Date = models.DateTimeField(
        null=True, blank=True)
    Notaria_VIII_VII_Date = models.DateTimeField(
        null=True, blank=True)
    Notaria_VIII_VIII_Date = models.DateTimeField(
        null=True, blank=True)
    Notaria_VIII_IX_Date = models.DateTimeField(
        null=True, blank=True)

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
        default=list,
        blank=True,  null=True)
    AprobacionCreditoState = models.NullBooleanField(
        blank=True, null=True,
        default=None)

    def __str__(self):
        return '%s-%s' % (self.EscrituraID, self.AprobacionCreditoID)