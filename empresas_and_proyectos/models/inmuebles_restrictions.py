import uuid
from django.db import models
from empresas_and_proyectos.models.inmuebles import Inmueble

# Models


class InmuebleInmuebleType(models.Model):
    InmuebleInmuebleTypeID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class InmuebleInmueble(models.Model):
    InmuebleAID = models.ForeignKey(
        Inmueble,
        related_name='inmueble_inmueble_a',
        on_delete=models.CASCADE)
    InmuebleBID = models.ForeignKey(
        Inmueble,
        related_name='inmueble_inmueble_b',
        on_delete=models.CASCADE)
    InmuebleInmuebleTypeID = models.ForeignKey(
        InmuebleInmuebleType,
        on_delete=models.CASCADE)

    def __str__(self):
        return '%s | %s, %s' % (self.InmuebleAID,
                                self.InmuebleBID,
                                self.InmuebleInmuebleTypeID)
