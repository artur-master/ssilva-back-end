from users.models import Permission
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    PermissionID = serializers.UUIDField()
    Name = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Permission
        fields = ('PermissionID', 'Name')
