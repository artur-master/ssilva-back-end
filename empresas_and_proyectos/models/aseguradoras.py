import uuid
from django.db import models


# Managers


class AseguradoraManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)

# Models


class Aseguradora(models.Model):
    AseguradoraID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=150)

    objects = AseguradoraManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return (self.Name,)
