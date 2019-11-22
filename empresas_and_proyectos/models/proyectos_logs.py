import uuid
from django.db import models

from empresas_and_proyectos.models.proyectos import Proyecto
from empresas_and_proyectos.pdf_filename import filename_proyecto_detail
from users.models import User

# Models


class ProyectoLogType(models.Model):
    ProyectoLogTypeID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=40)
    MaximunDays = models.IntegerField(default=0)

    def __str__(self):
        return self.Name


class ProyectoLog(models.Model):
    ProyectoLogID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    UserID = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    ProyectoID = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE)
    ProyectoLogTypeID = models.ForeignKey(
        ProyectoLogType,
        related_name='tipo_bitacora',
        on_delete=models.CASCADE)
    Counter = models.IntegerField(default=0)
    Date = models.DateTimeField(auto_now_add=True)
    Comment = models.CharField(
        max_length=150,
        null=True,
        blank=True)
    ProyectoDetailDocument = models.FileField(
        upload_to=filename_proyecto_detail,
        null=True,
        blank=True)

    def __str__(self):
        return '%s - %s - %s' % (self.ProyectoID,
                                 self.UserID, self.ProyectoLogTypeID.Name)