import uuid
from django.db import models

from empresas_and_proyectos.models.etapastate import EtapaState, EtapaManager
from empresas_and_proyectos.models.proyectos import Proyecto


class Etapa(models.Model):
    EtapaID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=40)
    SalesStartDate = models.DateTimeField(
        null=True,
        blank=True)
    EtapaStateID = models.ForeignKey(
        EtapaState,
        related_name="estado_etapa",
        on_delete=models.CASCADE)
    ProyectoID = models.ForeignKey(
        Proyecto,
        related_name='proyecto_etapa',
        on_delete=models.CASCADE)

    objects = EtapaManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return self.Name,