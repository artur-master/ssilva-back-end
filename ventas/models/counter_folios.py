from django.db import models

from empresas_and_proyectos.models.proyectos import Proyecto


class CounterFolio(models.Model):
    Count = models.IntegerField(default=1)
    ProyectoID = models.ForeignKey(
        Proyecto,
        related_name='proyecto_contador',
        on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.ProyectoID, self.Count)