from empresas_and_proyectos.models.constructoras import Constructora
from empresas_and_proyectos.models.inmobiliarias import (
    Inmobiliaria,
    InmobiliariaContactInfo,
    UserInmobiliariaType,
    UserInmobiliaria)
from users.models import User
from .inmobiliarias import (
    CreateInmobiliariaContactInfoSerializer,
    CreateUserInmobiliariaSerializer)
from common import constants
from common.models import ContactInfoType, Comuna
from common.validations import (validate_name_empresa, validate_rut_empresa)
from common.services import return_current_user, get_or_none
from common.notifications import (
    crear_notificacion_inmobiliaria_sin_representante,
    crear_notificacion_inmobiliaria_sin_aprobador)
from rest_framework import serializers


class ConstructoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constructora
        fields = ('ConstructoraID', 'RazonSocial', 'IsInmobiliaria',
                  'IsConstructora',)


class ConstructoraTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constructora
        fields = ('ConstructoraID', 'RazonSocial')


class CreateConstructoraSerializer(serializers.ModelSerializer):
    Contact = CreateInmobiliariaContactInfoSerializer(
        source='ContactInfo',
        many=True,
        required=False
    )
    UsersInmobiliaria = CreateUserInmobiliariaSerializer(
        source='UserInmobiliaria',
        many=True,
        required=False
    )
    RazonSocial = serializers.CharField(
        validators=[validate_name_empresa],
        required=False
    )
    Rut = serializers.CharField(
        validators=[validate_rut_empresa],
        required=False
    )
    Direccion = serializers.CharField(
        required=False
    )
    ComunaID = serializers.CharField(
        write_only=True,
        error_messages={
            "required": "Debe elegir una comuna"
        },
        required=False
    )
    Comuna = serializers.CharField(
        source='ComunaID.Name',
        read_only=True,
        required=False
    )
    IsInmobiliaria = serializers.BooleanField(
        write_only=True
    )

    class Meta:
        model = Constructora
        fields = ('ConstructoraID', 'RazonSocial', 'Rut',
                  'Direccion', 'ComunaID', 'Comuna',
                  'Contact', 'IsInmobiliaria', 'UsersInmobiliaria')

    def create(self, validated_data):
        current_user = return_current_user(self)

        is_inmobiliaria = validated_data.pop('IsInmobiliaria')

        if not is_inmobiliaria:
            instance = Constructora.objects.create(
                RazonSocial=validated_data['RazonSocial'],
                IsInmobiliaria=False,
                IsConstructora=True
            )
        else:
            contacts_info_data = validated_data.pop('ContactInfo')
            users_inmobiliaria_data = validated_data.pop('UserInmobiliaria')
            comuna = Comuna.objects.get(
                ComunaID=validated_data.pop('ComunaID'))

            instance = Constructora.objects.create(
                RazonSocial=validated_data['RazonSocial'],
                IsInmobiliaria=True,
                IsConstructora=True,
                State=True
            )

            inmobiliaria = Inmobiliaria.objects.create(
                InmobiliariaID=instance.ConstructoraID,
                ComunaID=comuna,
                Rut=validated_data['Rut'],
                RazonSocial=validated_data['RazonSocial'],
                Direccion=validated_data['Direccion'],
                IsConstructora=True,
                State=True
            )

            for contact_info_data in contacts_info_data:
                contact_info_type = ContactInfoType.objects.get(
                    ContactInfoTypeID=contact_info_data['ContactInfoTypeID'])

                InmobiliariaContactInfo.objects.create(
                    InmobiliariaID=inmobiliaria,
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
                    InmobiliariaID=inmobiliaria,
                    UserInmobiliariaTypeID=user_inmobiliaria_type
                )

            representante_inmobiliaria_type = UserInmobiliariaType.objects.get(
                Name=constants.USER_EMPRESA_TYPE[0])
            representante_inmobiliaria = UserInmobiliaria.objects.filter(
                InmobiliariaID=inmobiliaria,
                UserInmobiliariaTypeID=representante_inmobiliaria_type)

            if not representante_inmobiliaria.exists():
                crear_notificacion_inmobiliaria_sin_representante(
                    inmobiliaria, current_user)

            aprobador_inmobiliaria_type = UserInmobiliariaType.objects.get(
                Name=constants.USER_EMPRESA_TYPE[1])
            aprobador_inmobiliaria = UserInmobiliaria.objects.filter(
                InmobiliariaID=inmobiliaria, UserInmobiliariaTypeID=aprobador_inmobiliaria_type)

            if not aprobador_inmobiliaria.exists():
                crear_notificacion_inmobiliaria_sin_aprobador(
                    inmobiliaria, current_user)

        return instance


class UpdateConstructoraSerializer(serializers.ModelSerializer):
    Contact = CreateInmobiliariaContactInfoSerializer(
        source='ContactInfo',
        many=True,
        required=False
    )
    UsersInmobiliaria = CreateUserInmobiliariaSerializer(
        source='UserInmobiliaria',
        many=True,
        required=False
    )
    RazonSocial = serializers.CharField(
        validators=[validate_name_empresa],
        required=False
    )
    Rut = serializers.CharField(
        validators=[validate_rut_empresa],
        required=False
    )
    Direccion = serializers.CharField(
        required=False
    )
    ComunaID = serializers.CharField(
        write_only=True,
        error_messages={
            "required": "Debe elegir una comuna"
        },
        required=False
    )
    Comuna = serializers.CharField(
        source='ComunaID.Name',
        read_only=True,
        required=False
    )
    IsInmobiliaria = serializers.BooleanField(
        write_only=True
    )

    class Meta:
        model = Constructora
        fields = ('ConstructoraID', 'RazonSocial', 'Rut',
                  'Direccion', 'ComunaID', 'Comuna',
                  'Contact', 'IsInmobiliaria', 'UsersInmobiliaria')

    def update(self, instance, validated_data):
        current_user = return_current_user(self)

        is_inmobiliaria = validated_data.pop('IsInmobiliaria')

        inmobiliaria = get_or_none(
            Inmobiliaria, RazonSocial=instance.RazonSocial)

        if inmobiliaria:
            if not is_inmobiliaria:
                inmobiliaria.RazonSocial = validated_data.get(
                    'RazonSocial', inmobiliaria.RazonSocial)
                inmobiliaria.State = False
                inmobiliaria.save()
            else:
                comuna_id = validated_data.pop('ComunaID')
                users_inmobiliaria_data = validated_data.pop(
                    'UserInmobiliaria')
                contacts_info_data = validated_data.pop('ContactInfo')

                comuna = Comuna.objects.get(ComunaID=comuna_id)

                inmobiliaria.RazonSocial = validated_data.get(
                    'RazonSocial', inmobiliaria.RazonSocial)
                inmobiliaria.Rut = validated_data.get('Rut', inmobiliaria.Rut)
                inmobiliaria.Direccion = validated_data.get(
                    'Direccion', inmobiliaria.Direccion)
                inmobiliaria.ComunaID = comuna
                inmobiliaria.State = True

                contactos_inmobiliaria = InmobiliariaContactInfo.objects.filter(
                    InmobiliariaID=inmobiliaria)
                if contactos_inmobiliaria.exists():
                    contactos_inmobiliaria.delete()

                for contact_info_data in contacts_info_data:
                    contact_info_type = ContactInfoType.objects.get(
                        ContactInfoTypeID=contact_info_data['ContactInfoTypeID'])
                    value = contact_info_data['Value']

                    InmobiliariaContactInfo.objects.create(
                        InmobiliariaID=inmobiliaria,
                        ContactInfoTypeID=contact_info_type,
                        Value=value
                    )

                users_inmobiliaria = UserInmobiliaria.objects.filter(
                    InmobiliariaID=inmobiliaria)
                if users_inmobiliaria.exists():
                    users_inmobiliaria.delete()

                for user_inmobiliaria_data in users_inmobiliaria_data:
                    user_inmobiliaria_type = UserInmobiliariaType.objects.get(
                        Name=user_inmobiliaria_data['UserInmobiliariaTypeName'])
                    user_inmobiliaria = User.objects.get(
                        UserID=user_inmobiliaria_data['UserID'])

                    UserInmobiliaria.objects.create(
                        UserID=user_inmobiliaria,
                        InmobiliariaID=inmobiliaria,
                        UserInmobiliariaTypeID=user_inmobiliaria_type
                    )

                inmobiliaria.save()

                representante_inmobiliaria_type = UserInmobiliariaType.objects.get(
                    Name=constants.USER_EMPRESA_TYPE[0])
                representante_inmobiliaria = UserInmobiliaria.objects.filter(
                    InmobiliariaID=inmobiliaria, UserInmobiliariaTypeID=representante_inmobiliaria_type)

                if not representante_inmobiliaria.exists():
                    crear_notificacion_inmobiliaria_sin_representante(
                        inmobiliaria, current_user)

                aprobador_inmobiliaria_type = UserInmobiliariaType.objects.get(
                    Name=constants.USER_EMPRESA_TYPE[1])
                aprobador_inmobiliaria = UserInmobiliaria.objects.filter(
                    InmobiliariaID=inmobiliaria, UserInmobiliariaTypeID=aprobador_inmobiliaria_type)

                if not aprobador_inmobiliaria.exists():
                    crear_notificacion_inmobiliaria_sin_aprobador(
                        inmobiliaria, current_user)
        else:
            if is_inmobiliaria:
                comuna_id = validated_data.pop('ComunaID')
                users_inmobiliaria_data = validated_data.pop(
                    'UserInmobiliaria')
                contacts_info_data = validated_data.pop('ContactInfo')

                comuna = Comuna.objects.get(ComunaID=comuna_id)

                inmobiliaria = Inmobiliaria.objects.create(
                    InmobiliariaID=instance.ConstructoraID,
                    ComunaID=comuna,
                    Rut=validated_data['Rut'],
                    RazonSocial=instance.RazonSocial,
                    Direccion=validated_data['Direccion'],
                    IsConstructora=True,
                    State=True
                )

                for contact_info_data in contacts_info_data:
                    contact_info_type = ContactInfoType.objects.get(
                        ContactInfoTypeID=contact_info_data['ContactInfoTypeID'])

                    InmobiliariaContactInfo.objects.create(
                        InmobiliariaID=inmobiliaria,
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
                        InmobiliariaID=inmobiliaria,
                        UserInmobiliariaTypeID=user_inmobiliaria_type
                    )

                    representante_inmobiliaria_type = UserInmobiliariaType.objects.get(
                        Name=constants.USER_EMPRESA_TYPE[0])
                    representante_inmobiliaria = UserInmobiliaria.objects.filter(
                        InmobiliariaID=inmobiliaria, UserInmobiliariaTypeID=representante_inmobiliaria_type)

                    if not representante_inmobiliaria.exists():
                        crear_notificacion_inmobiliaria_sin_representante(
                            inmobiliaria, current_user)

                    aprobador_inmobiliaria_type = UserInmobiliariaType.objects.get(
                        Name=constants.USER_EMPRESA_TYPE[1])
                    aprobador_inmobiliaria = UserInmobiliaria.objects.filter(
                        InmobiliariaID=inmobiliaria, UserInmobiliariaTypeID=aprobador_inmobiliaria_type)

                if not aprobador_inmobiliaria.exists():
                    crear_notificacion_inmobiliaria_sin_aprobador(
                        inmobiliaria, current_user)

        instance.RazonSocial = validated_data.get(
            'RazonSocial', instance.RazonSocial)
        instance.IsInmobiliaria = is_inmobiliaria
        instance.save()

        return instance
