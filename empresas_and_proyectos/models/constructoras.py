import uuid
from django.db import models

# Managers


class ConstructoraManager(models.Manager):
    def get_by_natural_key(self, razon):
        return self.get(RazonSocial=razon)

# Models


class Constructora(models.Model):
    ConstructoraID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    RazonSocial = models.CharField(max_length=150)
    IsInmobiliaria = models.BooleanField(default=False)
    IsConstructora = models.BooleanField(default=True)
    State = models.BooleanField(default=True)

    objects = ConstructoraManager()

    def __str__(self):
        return self.RazonSocial

    def natural_key(self):
        return (self.RazonSocial,)