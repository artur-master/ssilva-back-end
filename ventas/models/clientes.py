from django.db import models
from django.contrib.postgres.fields import JSONField
from common.models import Comuna, ContactInfoType
from users.models import User
from empresas_and_proyectos.models.proyectos import Proyecto


class Cliente(User):
    Address = models.CharField(max_length=150)
    ComunaID = models.ForeignKey(
        Comuna,
        related_name="comuna_cliente",
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    CreationDate = models.DateTimeField(auto_now_add=True)
    Creator = models.ForeignKey(
        User,
        related_name="creator_cliente",
        on_delete=models.CASCADE)
    LastModificationDate = models.DateTimeField(auto_now=True)
    LastModifier = models.ForeignKey(
        User,
        related_name="last_modifier_cliente",
        on_delete=models.CASCADE)
    ContactInfo = models.ManyToManyField(
        ContactInfoType,
        related_name="contacto_cliente",
        through='ClienteContactInfo')
    Nationality = models.CharField(
        max_length=100,
        null=True,
        blank=True)
    Genre = models.CharField(
        max_length=100,
        null=True,
        blank=True)
    BirthDate = models.DateField(
        null=True,
        blank=True)
    CivilStatus = models.CharField(
        max_length=100,
        blank=True)
    Ocupation = models.CharField(
        max_length=100,
        blank=True)
    Position = models.CharField(
        max_length=100,
        blank=True)
    Carga = models.PositiveSmallIntegerField(default=0)
    Salary = models.PositiveIntegerField(default=0)
    TotalPatrimony = models.PositiveIntegerField(default=0)
    Antiquity = models.CharField(
        max_length=100,
        blank=True)
    ContractMarriageType = models.CharField(
        max_length=100,
        blank=True)
    IsDefinitiveResidence = models.BooleanField(default=False)
    IsCompany = models.BooleanField(default=False)
    Extra = JSONField(
        default=dict,
        blank=True,
        null=True)
    GiroEmpresa = models.CharField(
        max_length=250,
        blank=True) 
    ReprenetanteLegal = models.CharField(
        max_length=250,
        blank=True)     
    Proyecto = models.ManyToManyField(
        Proyecto,
        related_name='finding_way',
        through='ClienteProyecto',
        through_fields=(
            'UserID',
            'ProyectoID'))

    def __str__(self):
        return '%s %s' % (self.Name, self.LastNames)


class ClienteContactInfo(models.Model):
    UserID = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE)
    ContactInfoTypeID = models.ForeignKey(
        ContactInfoType,
        on_delete=models.CASCADE)
    Value = models.CharField(max_length=60)

    def __str__(self):
        return '%s - %s - %s' % (self.UserID,
                                 self.ContactInfoTypeID, self.Value)


class ClienteProyecto(models.Model):
    UserID = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE)
    ProyectoID = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE)
    FindingTypeID = models.ForeignKey(
        'FindingType',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return '%s - %s - %s' % (self.UserID,
                                 self.ProyectoID,
                                 self.FindingTypeID)
