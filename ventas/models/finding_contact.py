import uuid
from django.db import models


class FindingType(models.Model):
    FindingTypeID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=60)

    def __str__(self):
        return self.Name


class ContactMethodType(models.Model):
    ContactMethodTypeID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Name = models.CharField(max_length=60)

    def __str__(self):
        return self.Name
