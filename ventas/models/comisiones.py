import uuid
from django.db import models
from users.models import User
from empresas_and_proyectos.models.proyectos import Proyecto
# Para crear estos modelos ejecutar python manage.py makemigrations y luego
# python manage.py migrate
# Estos modelos no son definitivos pueden ser cambiados bajo criterio de ProductOwner



class MetaProyecto(models.Model):
    MetaID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    ProyectoID = models.ForeignKey(
        Proyecto,
        related_name='proyecto_meta',
        on_delete=models.CASCADE)
    Value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    # Mes de meta a ingresar
    DateMeta = models.DateTimeField(
        null=True,
        blank=True)

    def __str__(self):
        return '%s - %s' % (self.ProyectoID.Name, self.Value)


class ComisionVendedor(models.Model):
    ComisionVendedorID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    PromesaFirmadaID = models.ForeignKey(
        "PromesaFirmada",
        related_name='promesa_firmada_comision',
        on_delete=models.CASCADE)
    VendedorID = models.ForeignKey(
        User,
        related_name="vendedor_comision",
        on_delete=models.CASCADE)
    Porcentaje = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    ValorComisionID = models.ForeignKey(
        "ValorComision",
        related_name="valor_comision",
        on_delete=models.CASCADE)
    Date = models.DateTimeField(auto_now_add=True)
    DatePayment = models.DateTimeField(
    null=True,
    blank=True)
    State = models.CharField(max_length=50)
    # Mes de meta a ingresar
    DateMeta = models.DateTimeField(
        null=True,
        blank=True)


    def __str__(self):
        return '%s - %s' % (self.ProyectoID.Name, self.Value)


class PromesaFirmada(models.Model):
    PromesaFirmadaID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    VendedorID = models.ForeignKey(
        User,
        related_name="vendedor_promesa_firmada",
        on_delete=models.CASCADE)
    JefeProyectoID = models.ForeignKey(
        User,
        related_name="jefe_promesa_firmada",
        on_delete=models.CASCADE)
    ProyectoID = models.ForeignKey(
        Proyecto,
        related_name='proyecto_promesa_firmada',
        on_delete=models.CASCADE)
    FolioVenta = models.CharField(max_length=50)
    Value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    DateCreacion = models.DateTimeField(
        null=True,
        blank=True)
    DateCierre = models.DateTimeField(
        null=True,
        blank=True)
    Tipo = models.CharField(max_length=50)
    State = models.CharField(max_length=50)

    def __str__(self):
        return '%s - %s' % (self.ProyectoID.Name, self.State)


class ValorComision(models.Model):
    ValorComisionID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    IngresoPromesa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    DescuentoPromesa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    DeudaPendiente = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    DescuentoFinal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    DeudaFinal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    Bono = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    ValorFinal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    
    def __str__(self):
        return '%s' % (ValorComisionID)