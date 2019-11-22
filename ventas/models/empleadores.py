import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField


class Empleador(models.Model):
    EmpleadorID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Rut = models.CharField(unique=True, max_length=12, null=True, blank=True)
    RazonSocial = models.CharField(
        max_length=150,
        #unique=True,
        null=True,
        blank=True)
    Extra = JSONField(default=dict, blank=True)
    ClienteID = models.ForeignKey(
        'Cliente',
        related_name='cliente_empleador',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.EmpleadorID)
