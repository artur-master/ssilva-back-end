import uuid
from django.db import models


class EmpresaCompradora(models.Model):
    EmpresaCompradoraID = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    RazonSocial = models.CharField(
        max_length=150,
        #unique=True,
        null=True,
        blank=True)
    Rut = models.CharField(
        #unique=True,
        max_length=12,
        null=True,
        blank=True)
    Address = models.CharField(max_length=150, null=True, blank=True)
    ClienteID = models.ForeignKey(
        'Cliente',
        related_name='empresa_cliente',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.EmpresaCompradoraID)
