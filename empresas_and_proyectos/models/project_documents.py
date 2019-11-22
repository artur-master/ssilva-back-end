from datetime import datetime

from django.db import models
from django.utils import timezone

from common import constants
from users.models import User


def document_directory_path(instance, filename):
    return 'ProyectoDocuments/{0}/{1}/{2}'.format(instance.ProjectID, datetime.now().strftime("%Y-%m-%d"), filename)


class ProjectDocument(models.Model):
    Document = models.FileField(upload_to=document_directory_path, null=True, blank=True)
    DocumentType = models.CharField(null=False, max_length=50)
    State = models.CharField(choices=[
        (constants.DocumentState.TO_CONFIRM, 'To Confirm'),
        (constants.DocumentState.CONFIRMED, 'Confirmed'),
        (constants.DocumentState.REJECTED, 'Rejected')
    ], default='to_confirm', null=False, max_length=50)
    Poster = models.ForeignKey(
        to=User,
        related_name='user_document',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ProjectID = models.CharField(max_length=100, null=True)
    CreateAt = models.DateTimeField(default=timezone.now())
    NoExisted = models.BooleanField(default=False)

    def __str__(self):
        return self.Document.path
