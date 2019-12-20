import uuid
from django.db import models


class Condition(models.Model):
    ConditionID = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    Description = models.CharField(max_length=150, null=True,
        blank=True)
    IsImportant = models.BooleanField(default=False)
    IsApprove = models.BooleanField(default=False)
    def __str__(self):
        return self.Description

