import uuid
from django.db import models


# Managers


class InstitucionFinancieraManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)

# Models


class InstitucionFinanciera(models.Model):
    InstitucionFinancieraID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=150)

    objects = InstitucionFinancieraManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)
