from users.models import Role, Permission
from .permissions import PermissionSerializer
from common.validations import validate_name_role
from rest_framework import serializers


class RoleIDSerializer(serializers.ModelSerializer):
    RoleID = serializers.UUIDField()
    Name = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = Role
        fields = ('RoleID', 'Name')


class RoleNameIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('RoleID', 'Name')


class RoleSerializer(serializers.ModelSerializer):
    Permissions = PermissionSerializer(
        source='PermissionID',
        many=True
    )
    Name = serializers.CharField(
        validators=[validate_name_role]
    )

    class Meta:
        model = Role
        fields = ('RoleID', 'Name', 'Permissions')

    def create(self, validated_data):
        permissions_data = validated_data.pop('PermissionID')
        instance = Role.objects.create(**validated_data)

        for permission_data in permissions_data:
            permission = Permission.objects.get(
                PermissionID=permission_data['PermissionID'])
            instance.PermissionID.add(permission)

        return instance

    def update(self, instance, validated_data):
        permissions_data = validated_data.pop('PermissionID')

        instance.Name = validated_data.get('Name', instance.Name)

        # Se limpia la relación entre los permisos y el rol
        # para asi poder guardar las nuevas relaciones
        permission = instance.PermissionID
        permission.clear()

        for permission_data in permissions_data:
            permission = Permission.objects.get(
                PermissionID=permission_data['PermissionID'])
            instance.PermissionID.add(permission)

        instance.save()

        # Es necesario traer el objeto de nuevo para que se refleje
        # en la respuesta
        instance = self.Meta.model.objects.get(id=instance.id)

        return instance
