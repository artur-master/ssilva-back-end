import uuid
from django.db import models
from users.models import User

# Create your models here.

# Declaracion de manager los se ocupan para poder ocupar llaves naturales en los fixtures


class ContactInfoTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class RegionManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class ProvinciaManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class ComunaManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


# Declaracion de modelos


class Region(models.Model):
    RegionID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=40)

    # asignacion del manager a utilizar
    objects = RegionManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class Provincia(models.Model):
    ProvinciaID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    RegionID = models.ForeignKey(
        Region,
        related_name="region_provincia",
        on_delete=models.CASCADE)
    Name = models.CharField(max_length=40)

    # asignacion del manager a utilizar
    objects = ProvinciaManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class Comuna(models.Model):
    ComunaID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    ProvinciaID = models.ForeignKey(
        Provincia,
        related_name="provincia_comuna",
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    Name = models.CharField(max_length=40)

    # asignacion del manager a utilizar
    objects = ComunaManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class ContactInfoType(models.Model):
    ContactInfoTypeID = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=10)

    # asignacion del manager a utilizar
    objects = ContactInfoTypeManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class NotificationType(models.Model):
    NotificationTypeID = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=60)
    TableName = models.CharField(max_length=20)
    RedirectRouteName = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class Notification(models.Model):
    NotificationID = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    NotificationTypeID = models.ForeignKey(
        NotificationType,
        related_name="notification_type",
        on_delete=models.CASCADE)
    TableID = models.UUIDField(editable=True)
    UserID = models.ManyToManyField(User, related_name='user_notification')
    CreationDate = models.DateTimeField(auto_now_add=True)
    Message = models.CharField(max_length=140)
    RedirectRouteID = models.UUIDField(editable=True, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.Message)


class APIUpdate(models.Model):
    Name = models.CharField(max_length=20)
    Date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.Name, self.Date)


class UF(models.Model):
    Date = models.DateField()
    Value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '%s - %s' % (self.Date, self.Value)


class ConstantNumeric(models.Model):
    Name = models.CharField(max_length=20)
    Value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '%s - %s' % (self.Name, self.Value)
