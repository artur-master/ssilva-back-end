from django.contrib.auth.models import User as UserDjango
from django.core.exceptions import ValidationError

from users.models import User, Role
from common import constants
from common.models import NotificationType, Notification
from common.serializers import notifications
from common.notifications import crear_notificacion_cambio_clave
from common.services import enviar_contrasena_por_email, generar_contrasena
from common.validations import validate_rut_usuario, validate_email_usuario
from .roles import RoleNameIDSerializer, RoleIDSerializer
from rest_framework import serializers


class UserProfilePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('UserID', 'Name', 'LastNames', 'Rut')


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        style={'input_type': 'password'},
        required=True
    )
    new_password = serializers.CharField(
        style={'input_type': 'password'},
        required=True
    )
    confirm_password = serializers.CharField(
        style={'input_type': 'password'},
        required=True
    )

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_password')


class ListResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('UserID', 'Name', 'LastNames')


class UserProfileListSerializer(serializers.ModelSerializer):
    Roles = RoleNameIDSerializer(
        source='RoleID',
        many=True
    )
    IsActive = serializers.BooleanField(
        source='DjangoUser.is_active',
        read_only=True
    )
    Notifications = serializers.SerializerMethodField('get_notificaciones')

    class Meta:
        model = User
        fields = ('UserID', 'Name', 'LastNames',
                  'Rut', 'IsActive', 'Roles',
                  'Notifications')

    def get_notificaciones(self, obj):
        notification_type = NotificationType.objects.get(
            Name=constants.NOTIFICATION_TYPE[8])
        notificacions = Notification.objects.filter(
            TableID=obj.UserID, NotificationTypeID=notification_type)
        serializer = notifications.NotificationSerializer(instance=notificacions, many=True)
        return serializer.data


class UserProfileSerializer(serializers.ModelSerializer):
    Roles = RoleIDSerializer(
        source='RoleID',
        many=True
    )
    
    IsActive = serializers.BooleanField(
        source='DjangoUser.is_active',
        read_only=True
    )

    class Meta:
        model = User
        fields = ('UserID', 'Name', 'LastNames',
                  'Rut', 'Email', 'IsActive', 'Roles')

    @staticmethod
    def create_django_user(validated_data, skip_error=False):
        if 'Rut' not in validated_data or 'Email' not in validated_data and not skip_error:
            raise ValidationError('Fields Rut and Email must not be empty')
        try:
            django_user = UserDjango.objects.create(
                username=validated_data['Rut'],
                first_name=validated_data.get('Name', str()),
                last_name=validated_data.get('LastNames', str()),
                email=validated_data['Email']
            )

            user_password = generar_contrasena()
            django_user.set_password(user_password)
            django_user.save()
            return django_user, user_password
        except Exception as ex:
            if skip_error:
                return None, None
            raise ValidationError("Failed to create new user %s" % str(ex))

    def create(self, validated_data):
        roles_data = validated_data.pop('RoleID')

        django_user, user_password = self.create_django_user(validated_data)

        instance = User.objects.create(
            DjangoUser=django_user,
            **validated_data
        )
        if django_user:
            enviar_contrasena_por_email(instance, user_password)

        for role_data in roles_data:
            role = Role.objects.get(RoleID=role_data['RoleID'])
            instance.RoleID.add(role)

        crear_notificacion_cambio_clave(instance)

        return instance

    def update(self, instance, validated_data):
        if(instance.Rut != validated_data.get('Rut', instance.Rut)):
            instance.Rut = validated_data.get('Rut', instance.Rut)
        instance.Name = validated_data.get('Name', instance.Name)
        instance.LastNames = validated_data.get('LastNames', instance.LastNames)
        instance.Email = validated_data.get('Email', instance.Email)

        if not instance.DjangoUser:
            validated_data['Rut'] = instance.Rut
            validated_data['Email'] = validated_data.get('Email', instance.Email)
            django_user, user_password = self.create_django_user(validated_data, skip_error=True)
            instance.DjangoUser = django_user
        else:
            instance.DjangoUser.first_name = validated_data.get('Name', instance.Name)
            instance.DjangoUser.last_name = validated_data.get('LastNames', instance.LastNames)
            instance.DjangoUser.email = validated_data.get('Email', instance.Email)
            instance.DjangoUser.username = validated_data.get('Rut', instance.Rut)

        # Se limpia la relación entre los roles y el usuario
        # para asi poder guardar las nuevas relaciones
        roles_data = validated_data.get('RoleID')
        if roles_data:
            role = instance.RoleID
            role.clear()

            for role_data in roles_data:
                role = Role.objects.get(RoleID=role_data['RoleID'])
                instance.RoleID.add(role)

        instance.save()
        instance.DjangoUser.save()

        # # Es necesario traer el objeto de nuevo para que se refleje
        # # en la respuesta
        return instance
