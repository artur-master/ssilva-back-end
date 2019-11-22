import uuid
from django.db import models
from empresas_and_proyectos.models.etapas import Etapa

# Managers


class EdificioManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)

# Models


class Edificio(models.Model):
    EdificioID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=255, blank=True)
    EtapaID = models.ForeignKey(
        Etapa,
        related_name='etapa_edificio',
        on_delete=models.CASCADE)

    objects = EdificioManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)
