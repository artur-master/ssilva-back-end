import uuid
from django.db import models

# Managers


class PlanMediosStateManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class BorradorPromesaStateManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class IngresoComisionesStateManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


# Models


class PlanMediosState(models.Model):
    PlanMediosStateID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=40)

    objects = PlanMediosStateManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class BorradorPromesaState(models.Model):
    BorradorPromesaStateID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=40)

    objects = BorradorPromesaStateManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)


class IngresoComisionesState(models.Model):
    IngresoComisionesStateID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=40)

    objects = IngresoComisionesStateManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)

