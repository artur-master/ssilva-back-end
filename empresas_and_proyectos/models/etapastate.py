# -*- coding: utf-8 -*-
import uuid
from django.db import models


class EtapaStateManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class EtapaManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(Name=name)


class EtapaState(models.Model):
    EtapaStateID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=40)

    objects = EtapaStateManager()

    def __str__(self):
        return self.Name

    def natural_key(self):
        return self.Name,
