from empresas_and_proyectos.models.constructoras import Constructora
from empresas_and_proyectos.models.inmobiliarias import (
    Inmobiliaria,
    InmobiliariaContactInfo,
    UserInmobiliaria,
    UserInmobiliariaType)
from common import constants
from common.models import Notification, Comuna, ContactInfoType
from users.models import User
from common.serializers.notifications import NotificationSerializer
from common.services import return_current_user, get_or_none
from common.validations import (
    CustomValidation,
    validate_name_empresa,
    validate_rut_empresa)
from common.notifications import (
    crear_notificacion_inmobiliaria_sin_representante,
    crear_notificacion_inmobiliaria_sin_aprobador,
    eliminar_notificacion_inmobiliaria_sin_representante,
    eliminar_notificacion_inmobiliaria_sin_aprobador)
from rest_framework import serializers, status


class InmobiliariaContactInfoSerializer(serializers.ModelSerializer):
    InmobiliariaID = serializers.UUIDField(
        write_only=True
    )
    Inmobiliaria = serializers.CharField(
        source='InmobiliariaID.InmobiliariaID',
        read_only=True,
        required=False
    )
    ContactInfoTypeID = serializers.UUIDField(
        write_only=True
    )
    ContactInfoType = serializers.CharField(
        source='ContactInfoTypeID.ContactInfoTypeID',
        read_only=True
    )
    ContactInfoTypeName = serializers.CharField(
        source='ContactInfoTypeID.Name',
        read_only=True
    )

    class Meta:
        model = InmobiliariaContactInfo
        fields = ('InmobiliariaID', 'Inmobiliaria', 'ContactInfoTypeID',
                  'ContactInfoType', 'ContactInfoTypeName', 'Value')


class InmobiliariaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inmobiliaria
        fields = ('InmobiliariaID', 'RazonSocial')


class InmobiliariaSerializer(serializers.ModelSerializer):
    Comuna = serializers.CharField(
        source='ComunaID.Name',
        read_only=True
    )
    ComunaID = serializers.CharField(
        source='ComunaID.ComunaID',
        read_only=True
    )
    Provincia = serializers.CharField(
        source='ComunaID.ProvinciaID.Name',
        read_only=True
    )
    Region = serializers.CharField(
        source='ComunaID.ProvinciaID.RegionID.Name',
        read_only=True
    )

    Notifications = serializers.SerializerMethodField('get_notificaciones')
    Contact = serializers.SerializerMethodField('get_contactos')
    UsersInmobiliaria = serializers.SerializerMethodField(
        'get_users_inmobiliaria')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('ComunaID')
        queryset = queryset.prefetch_related('ContactInfo', 'UserInmobiliaria')
        return queryset

    class Meta:
        model = Inmobiliaria
        fields = ('InmobiliariaID', 'RazonSocial', 'Rut', 'Direccion',
                  'Provincia', 'ComunaID', 'Comuna', 'Region', 'Contact', 'IsConstructora',
                  'IsInmobiliaria', 'UsersInmobiliaria', 'Notifications')

    def get_notificaciones(self, obj):
        notifications = Notification.objects.filter(
            TableID=obj.InmobiliariaID,
            UserID__DjangoUser__username=self.context['request'].user)
        serializer = NotificationSerializer(instance=notifications, many=True)
        return serializer.data

    def get_contactos(self, obj):
        contactos = InmobiliariaContactInfo.objects.filter(InmobiliariaID=obj)
        serializer = InmobiliariaContactInfoSerializer(
            instance=contactos, many=True)
        return serializer.data

    def get_users_inmobiliaria(self, obj):
        users_inmobiliaria = UserInmobiliaria.objects.filter(
            InmobiliariaID=obj)
        serializer = UserInmobiliariaSerializer(
            instance=users_inmobiliaria, many=True)
        return serializer.data


class UserInmobiliariaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInmobiliariaType
        fields = ('UserInmobiliariaTypeID', 'Name')


class UserInmobiliariaSerializer(serializers.ModelSerializer):
    Name = serializers.CharField(
        source='UserID.Name',
        read_only=True
    )
    LastNames = serializers.CharField(
        source='UserID.LastNames',
        read_only=True
    )
    Rut = serializers.CharField(
        source='UserID.Rut',
        read_only=True
    )
    UserID = serializers.CharField(
        source='UserID.UserID',
        read_only=True
    )
    UserInmobiliariaType = serializers.CharField(
        source='UserInmobiliariaTypeID.Name',
        read_only=True
    )
    UserInmobiliariaTypeID = serializers.CharField(
        source='UserInmobiliariaTypeID.UserInmobiliariaTypeID',
        read_only=True
    )

    class Meta:
        model = UserInmobiliaria
        fields = ('UserID', 'Name', 'LastNames', 'Rut',
                  'UserInmobiliariaTypeID', 'UserInmobiliariaType')


class CreateUserInmobiliariaSerializer(serializers.ModelSerializer):
    Inmobiliaria = serializers.CharField(
        source='InmobiliariaID',
        read_only=True
    )
    UserID = serializers.UUIDField(
        write_only=True
    )
    User = serializers.CharField(
        source='UserID',
        read_only=True
    )
    UserInmobiliariaTypeName = serializers.CharField(
        write_only=True
    )
    UserInmobiliariaType = serializers.CharField(
        source='UserInmobiliariaTypeID.Name',
        read_only=True
    )

    class Meta:
        model = UserInmobiliaria
        fields = ('Inmobiliaria', 'UserID', 'User',
                  'UserInmobiliariaTypeName', 'UserInmobiliariaType')


class CreateInmobiliariaContactInfoSerializer(serializers.ModelSerializer):
    Inmobiliaria = serializers.CharField(
        source='InmobiliariaID.Name',
        read_only=True
    )
    ContactInfoTypeID = serializers.UUIDField(
        write_only=True
    )
    ContactInfoType = serializers.CharField(
        source='ContactInfoTypeID',
        read_only=True
    )
    Value = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = InmobiliariaContactInfo
        fields = (
            'Inmobiliaria',
            'ContactInfoTypeID',
            'ContactInfoType',
            'Value')


class CreateInmobiliariaSerializer(serializers.ModelSerializer):
    Contact = CreateInmobiliariaContactInfoSerializer(
        source='ContactInfo',
        many=True
    )
    UsersInmobiliaria = CreateUserInmobiliariaSerializer(
        source='UserInmobiliaria',
        many=True
    )
    RazonSocial = serializers.CharField(
        validators=[validate_name_empresa]
    )
    Rut = serializers.CharField(
        validators=[validate_rut_empresa]
    )
    ComunaID = serializers.CharField(
        write_only=True,
        error_messages={
            "required": "Debe elegir una comuna"
        }
    )
    Comuna = serializers.CharField(
        source='ComunaID.Name',
        read_only=True
    )
    IsConstructora = serializers.BooleanField(
        write_only=True
    )

    class Meta:
        model = Inmobiliaria
        fields = ('InmobiliariaID', 'RazonSocial', 'Rut',
                  'Direccion', 'ComunaID', 'Comuna',
                  'Contact', 'IsConstructora', 'UsersInmobiliaria')

    def create(self, validated_data):
        current_user = return_current_user(self)

        contacts_info_data = validated_data.pop('ContactInfo')
        users_inmobiliaria_data = validated_data.pop('UserInmobiliaria')
        is_constructora = validated_data['IsConstructora']

        comuna = Comuna.objects.get(ComunaID=validated_data.pop('ComunaID'))

        if not is_constructora:
            instance = Inmobiliaria.objects.create(
                ComunaID=comuna,
                Rut=validated_data['Rut'],
                RazonSocial=validated_data['RazonSocial'],
                Direccion=validated_data['Direccion'],
                IsInmobiliaria=True,
                IsConstructora=False,
                State=True
            )

            for contact_info_data in contacts_info_data:
                contact_info_type = ContactInfoType.objects.get(
                    ContactInfoTypeID=contact_info_data['ContactInfoTypeID'])

                InmobiliariaContactInfo.objects.create(
                    InmobiliariaID=instance,
                    ContactInfoTypeID=contact_info_type,
                    Value=contact_info_data['Value']
                )

            for user_inmobiliaria_data in users_inmobiliaria_data:
                user_inmobiliaria_type = UserInmobiliariaType.objects.get(
                    Name=user_inmobiliaria_data['UserInmobiliariaTypeName'])
                user_inmobiliaria = User.objects.get(
                    UserID=user_inmobiliaria_data['UserID'])

                UserInmobiliaria.objects.create(
                    UserID=user_inmobiliaria,
                    InmobiliariaID=instance,
                    UserInmobiliariaTypeID=user_inmobiliaria_type
                )
        else:
            instance = Inmobiliaria.objects.create(
                ComunaID=comuna,
                Rut=validated_data['Rut'],
                RazonSocial=validated_data['RazonSocial'],
                Direccion=validated_data['Direccion'],
                IsInmobiliaria=True,
                IsConstructora=True,
                State=True
            )

            for contact_info_data in contacts_info_data:
                contact_info_type = ContactInfoType.objects.get(
                    ContactInfoTypeID=contact_info_data['ContactInfoTypeID'])

                InmobiliariaContactInfo.objects.create(
                    InmobiliariaID=instance,
                    ContactInfoTypeID=contact_info_type,
                    Value=contact_info_data['Value']
                )

            for user_inmobiliaria_data in users_inmobiliaria_data:
                user_inmobiliaria_type = UserInmobiliariaType.objects.get(
                    Name=user_inmobiliaria_data['UserInmobiliariaTypeName'])
                user_inmobiliaria = User.objects.get(
                    UserID=user_inmobiliaria_data['UserID'])

                UserInmobiliaria.objects.create(
                    UserID=user_inmobiliaria,
                    InmobiliariaID=instance,
                    UserInmobiliariaTypeID=user_inmobiliaria_type
                )

            Constructora.objects.create(
                ConstructoraID=instance.InmobiliariaID,
                RazonSocial=validated_data['RazonSocial'],
                IsInmobiliaria=True,
                State=True
            )

        representante_inmobiliaria_type = UserInmobiliariaType.objects.get(
            Name=constants.USER_EMPRESA_TYPE[0])
        representante_inmobiliaria = UserInmobiliaria.objects.filter(
            InmobiliariaID=instance, UserInmobiliariaTypeID=representante_inmobiliaria_type)

        if not representante_inmobiliaria.exists():
            crear_notificacion_inmobiliaria_sin_representante(
                instance, current_user)

        aprobador_inmobiliaria_type = UserInmobiliariaType.objects.get(
            Name=constants.USER_EMPRESA_TYPE[1])
        aprobador_inmobiliaria = UserInmobiliaria.objects.filter(
            InmobiliariaID=instance, UserInmobiliariaTypeID=aprobador_inmobiliaria_type)

        if not aprobador_inmobiliaria.exists():
            crear_notificacion_inmobiliaria_sin_aprobador(
                instance, current_user)

        return instance


class UpdateInmobiliariaSerializer(serializers.ModelSerializer):
    Contact = CreateInmobiliariaContactInfoSerializer(
        source='ContactInfo',
        many=True
    )
    UsersInmobiliaria = CreateUserInmobiliariaSerializer(
        source='UserInmobiliaria',
        many=True
    )
    RazonSocial = serializers.CharField(
        validators=[validate_name_empresa]
    )
    Rut = serializers.CharField(
        read_only=True,
        validators=[validate_rut_empresa]
    )
    ComunaID = serializers.CharField(
        write_only=True,
        error_messages={
            "required": "Debe elegir una comuna"
        }
    )
    Comuna = serializers.CharField(
        source='ComunaID.Name',
        read_only=True
    )
    IsConstructora = serializers.BooleanField(
        write_only=True
    )

    class Meta:
        model = Inmobiliaria
        fields = ('InmobiliariaID', 'RazonSocial', 'Rut',
                  'Direccion', 'ComunaID', 'Comuna',
                  'Contact', 'IsConstructora', 'UsersInmobiliaria')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        users_inmobiliaria_data = validated_data.pop('UserInmobiliaria')
        contacts_info_data = validated_data.pop('ContactInfo')
        is_constructora = validated_data.pop('IsConstructora')

        comuna = Comuna.objects.get(
            ComunaID=validated_data.pop(
                'ComunaID', instance.ComunaID))

        constructora = get_or_none(
            Constructora, RazonSocial=instance.RazonSocial)

        if constructora:
            if not is_constructora:
                constructora.RazonSocial = validated_data.get(
                    'RazonSocial', constructora.RazonSocial)
                constructora.IsInmobiliaria = False
                constructora.State = False
                constructora.save()
            else:
                constructora.RazonSocial = validated_data.get(
                    'RazonSocial', constructora.RazonSocial)
                constructora.IsInmobiliaria = True
                constructora.State = True
                constructora.save()
        else:
            Constructora.objects.create(
                ConstructoraID=instance.InmobiliariaID,
                RazonSocial=instance.RazonSocial,
                IsInmobiliaria=True,
                State=True
            )

        instance.RazonSocial = validated_data.get(
            'RazonSocial', instance.RazonSocial)
        instance.Direccion = validated_data.get(
            'Direccion', instance.Direccion)
        instance.ComunaID = comuna
        instance.IsConstructora = is_constructora

        contactos_inmobiliaria = InmobiliariaContactInfo.objects.filter(
            InmobiliariaID=instance)
        if contactos_inmobiliaria.exists():
            contactos_inmobiliaria.delete()

        for contact_info_data in contacts_info_data:
            contact_info_type = ContactInfoType.objects.get(
                ContactInfoTypeID=contact_info_data['ContactInfoTypeID'])
            value = contact_info_data['Value']

            InmobiliariaContactInfo.objects.create(
                InmobiliariaID=instance,
                ContactInfoTypeID=contact_info_type,
                Value=value
            )

        users_inmobiliaria = UserInmobiliaria.objects.filter(
            InmobiliariaID=instance)
        if users_inmobiliaria.exists():
            users_inmobiliaria.delete()

        for user_inmobiliaria_data in users_inmobiliaria_data:
            user_inmobiliaria_type = UserInmobiliariaType.objects.get(
                Name=user_inmobiliaria_data['UserInmobiliariaTypeName'])
            user_inmobiliaria = User.objects.get(
                UserID=user_inmobiliaria_data['UserID'])

            UserInmobiliaria.objects.create(
                UserID=user_inmobiliaria,
                InmobiliariaID=instance,
                UserInmobiliariaTypeID=user_inmobiliaria_type
            )

        instance.save()

        representante_inmobiliaria_type = UserInmobiliariaType.objects.get(
            Name=constants.USER_EMPRESA_TYPE[0])
        representante_inmobiliaria = UserInmobiliaria.objects.filter(
            InmobiliariaID=instance, UserInmobiliariaTypeID=representante_inmobiliaria_type)

        if not representante_inmobiliaria.exists():
            crear_notificacion_inmobiliaria_sin_representante(
                instance, current_user)
        else:
            eliminar_notificacion_inmobiliaria_sin_representante(instance)

        aprobador_inmobiliaria_type = UserInmobiliariaType.objects.get(
            Name=constants.USER_EMPRESA_TYPE[1])
        aprobador_inmobiliaria = UserInmobiliaria.objects.filter(
            InmobiliariaID=instance, UserInmobiliariaTypeID=aprobador_inmobiliaria_type)

        if not aprobador_inmobiliaria.exists():
            crear_notificacion_inmobiliaria_sin_aprobador(
                instance, current_user)
        else:
            eliminar_notificacion_inmobiliaria_sin_aprobador(instance)

        return instance
