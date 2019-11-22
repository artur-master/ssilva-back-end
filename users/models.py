import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PermissionManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class RoleManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class UserManager(models.Manager):
    def get_by_natural_key(self, rut):
        return self.get(Rut=rut)


class NationalityManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Permission(models.Model):
    PermissionID = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=40)

    objects = PermissionManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class Role(models.Model):
    RoleID = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=40)
    PermissionID = models.ManyToManyField(
        Permission, related_name='permission_role')

    objects = RoleManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class User(models.Model):
    UserID = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=40, null=True, blank=True)
    LastNames = models.CharField(max_length=60, null=True, blank=True)
    Rut = models.CharField(max_length=12, null=True, blank=True)
    Email = models.EmailField(max_length=60, null=True, blank=True)
    RoleID = models.ManyToManyField(Role, related_name='role_user', blank=True)
    DjangoUser = models.OneToOneField(
        "auth.User",
        on_delete=models.CASCADE,
        related_name='user',
        blank=True,
        null=True)

    objects = UserManager()

    def __str__(self):
        return '%s %s' % (self.Name, self.LastNames)

    def natural_key(self):
        return (self.Rut,)


class Nationality(models.Model):
    code = models.CharField(max_length=3, unique=True, db_index=True)
    name = models.CharField(max_length=50)

    objects = NationalityManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.code,)
