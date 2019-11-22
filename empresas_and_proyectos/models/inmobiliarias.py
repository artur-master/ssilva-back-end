import uuid
from django.db import models
from users.models import User
from common.models import Comuna, ContactInfoType


# Managers


class InmobiliariaManager(models.Manager):
    def get_by_natural_key(self, razon):
        return self.get(RazonSocial=razon)


class UserInmobiliariaTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)
# Models


class Inmobiliaria(models.Model):
    InmobiliariaID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    ComunaID = models.ForeignKey(
        Comuna,
        related_name="comuna_empresa",
        on_delete=models.CASCADE)
    Rut = models.CharField(
        unique=True,
        max_length=12)
    ContactInfo = models.ManyToManyField(
        ContactInfoType,
        related_name="contacto_empresa",
        through='InmobiliariaContactInfo')
    RazonSocial = models.CharField(
        max_length=150,
        unique=True)
    Direccion = models.CharField(max_length=150)
    UserInmobiliaria = models.ManyToManyField(
        User,
        related_name='user_inmobiliaria',
        through='UserInmobiliaria')
    IsInmobiliaria = models.BooleanField(default=True)
    IsConstructora = models.BooleanField(default=False)
    State = models.BooleanField(default=True)

    objects = InmobiliariaManager()

    def __str__(self):
        return self.RazonSocial

    def natural_key(self):
        return (self.RazonSocial,)


class UserInmobiliariaType(models.Model):
    UserInmobiliariaTypeID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=40)

    objects = UserInmobiliariaTypeManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class UserInmobiliaria(models.Model):
    UserID = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    InmobiliariaID = models.ForeignKey(
        Inmobiliaria,
        on_delete=models.CASCADE)
    UserInmobiliariaTypeID = models.ForeignKey(
        UserInmobiliariaType,
        on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s - %s' % (self.UserID,
                                 self.InmobiliariaID,
                                 self.UserInmobiliariaTypeID)


class InmobiliariaContactInfo(models.Model):
    InmobiliariaID = models.ForeignKey(
        Inmobiliaria,
        on_delete=models.CASCADE)
    ContactInfoTypeID = models.ForeignKey(
        ContactInfoType,
        on_delete=models.CASCADE)
    Value = models.CharField(max_length=60)

    def __str__(self):
        return '%s - %s - %s' % (self.InmobiliariaID,
                                 self.ContactInfoTypeID, self.Value)

