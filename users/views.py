import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User as UserDjango
from django.contrib.auth import authenticate, update_session_auth_hash
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import *
from empresas_and_proyectos.models.constructoras import Constructora
from empresas_and_proyectos.models.inmobiliarias import (
    Inmobiliaria,
    UserInmobiliariaType,
    UserInmobiliaria)
from common import constants
from common.models import (
    Region,
    Provincia,
    Comuna,
    NotificationType,
    Notification,
    ContactInfoType,
    UF,
    ConstantNumeric)
from common.serializers.notifications import NotificationSerializer
from common.serializers.regiones import RegionSerializer
from common.serializers.provincias import ProvinciaSerializer
from common.serializers.comunas import ComunaSerializer
from common.serializers.contacts_info import ContactInfoTypeSerializer
from common.serializers.ufs import UFSerializer
from common.serializers.constants_numerics import ConstantNumericSerializer
from .serializers.permissions import PermissionSerializer
from .serializers.roles import RoleSerializer
from .serializers.users import (
    UserProfilePermissionSerializer,
    UserProfileSerializer,
    UserProfileListSerializer,
    ChangePasswordSerializer)
from .serializers.inmobiliarias import (
    InmobiliariaSerializer,
    CreateInmobiliariaSerializer,
    UpdateInmobiliariaSerializer,
    UserInmobiliariaTypeSerializer,
    UserInmobiliariaSerializer)
from .serializers.constructoras import (
    ConstructoraSerializer,
    CreateConstructoraSerializer,
    UpdateConstructoraSerializer)
from common.permissions import (
    CheckAdminRolePermission,
    CheckAdminOrConsRolePermission,
    IsOwnerUserProfile,
    CheckAdminUsersPermission,
    CheckAdminInmobOrAdminParamPermission,
    CheckAdminOrConsUsersPermission,
    CheckAdminInmobPermission,
    CheckAdminOrConsInmobPermission,
    CheckAdminOrConsInmobOrConsParamPermission)
from common.services import (
    validar_rut,
    validar_contrasena,
    generar_contrasena,
    enviar_contrasena_por_email)
from common.notifications import (
    crear_notificacion_cambio_clave,
    eliminar_notificacion_cambio_clave)
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
# Create your views here.


class PermissionViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()


class UserPermissionViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PermissionSerializer

    def get_queryset(self):
        queryset = Permission.objects.filter(
            permission_role__role_user__Rut=self.request.user
        ).distinct()

        return queryset


class UserProfilePermissionViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfilePermissionSerializer

    def get_queryset(self):
        permission_name = self.request.query_params.get('q', None)
        permission = Permission.objects.get(Name=permission_name)
        queryset = User.objects.filter(
            RoleID__PermissionID=permission
        ).distinct()

        return queryset


class RolePermissionViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    lookup_field = 'RoleID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            # permission_classes = [
            #     IsAuthenticated, CheckAdminOrConsRolePermission, ]
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, CheckAdminRolePermission, ]
        return [permission() for permission in permission_classes]

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response({"role": serializer.data,
                             "detail": "Rol creado con éxito"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)

    def partial_update(self, request, RoleID):
        role = self.get_object()
        serializer = self.get_serializer(role, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"role": serializer.data,
                             "detail": "Rol modificado con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        rut = request.data.get("rut")
        password = request.data.get("password")

        if rut is None or password is None:
            return Response({'detail': 'Ingrese ambos campos'},
                            status=status.HTTP_409_CONFLICT)

        #if not validar_rut(rut):
        #    return Response({'detail': 'Rut Inválido'},
        #                    status=status.HTTP_409_CONFLICT)

        user = authenticate(username=rut, password=password)

        if not user:
            return Response({'detail': 'Credenciales Incorrectas, intenta nuevamente'},
                            status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)

        user_model = get_object_or_404(User, DjangoUser=user)

        permissions = Permission.objects.filter(
            permission_role__role_user=user_model.id
        ).distinct()

        user_permissions = [
            permission.Name
            for permission in permissions
        ]

        return Response({'token': token.key,
                         'user_id': user_model.UserID,
                         'user_permissions': user_permissions},
                        status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated, IsOwnerUserProfile,)
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    lookup_field = 'UserID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # if self.action == 'retrieve':
            # permission_classes = [IsAuthenticated, IsOwnerUserProfile, ]
        # elif self.action == 'list':
        #     permission_classes = [IsAuthenticated,
        #                           CheckAdminOrConsUsersPermission, ]
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, CheckAdminUsersPermission, ]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserProfileListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = UserProfileSerializer(data=data, many=many)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response({"user": serializer.data,
                             "detail": "Usuario creado con éxito"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)

    def partial_update(self, request, UserID):
        serializer = UserProfileSerializer(
            self.get_object(), data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"user": serializer.data,
                             "detail": "Usuario modificado con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class UpdatePasswordAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_pass = serializer.data.get("new_password")
            confirm_password = serializer.data.get("confirm_password")

            if not self.object.check_password(old_password):
                return Response({"detail": "Contraseña actual incorrecta"},
                                status=status.HTTP_409_CONFLICT)

            if validar_contrasena(new_pass):
                if new_pass == confirm_password:
                    self.object.set_password(new_pass)
                    self.object.save()
                    update_session_auth_hash(request, self.object)

                    eliminar_notificacion_cambio_clave(self.object)

                    return Response({"detail": "Contraseña actualizada con éxito"},
                                    status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({"detail": "Contraseñas no coinciden"},
                                    status=status.HTTP_409_CONFLICT)
            else:
                return Response(
                    {"detail": "Contraseña debe contener al menos 7 caracteres, 1 letra y un número"},
                    status=status.HTTP_409_CONFLICT)

        return Response({"detail": constants.GENERIC_MESSAGE},
                        status=status.HTTP_400_BAD_REQUEST)


class ActiveDisableUserAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminUsersPermission,)

    def get(request, self, user_id):
        user = User.objects.get(UserID=user_id)
        django_user = UserDjango.objects.get(user=user)

        if django_user.is_active:
            django_user.is_active = False
            django_user.save()

            token = Token.objects.filter(user=django_user)
            if token.exists():
                token.delete()

            return Response({"active": django_user.is_active},
                            status=status.HTTP_200_OK)

        else:
            django_user.is_active = True
            django_user.save()
            return Response({"active": django_user.is_active},
                            status=status.HTTP_200_OK)


class ResetPasswordUserAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminUsersPermission,)

    def get(request, self, user_id):
        user = User.objects.get(UserID=user_id)
        django_user = UserDjango.objects.get(user=user)

        new_password = generar_contrasena()
        django_user.set_password(new_password)
        django_user.save()

        enviar_contrasena_por_email(user, new_password)
        crear_notificacion_cambio_clave(user)

        return Response({"detail": "Contraseña ha sido reseteada y enviada al usuario"},
                        status=status.HTTP_200_OK)


class UserNotificationViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = Notification.objects.filter(UserID__Rut=self.request.user)
        return queryset


class InmobiliariaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = InmobiliariaSerializer
    queryset = Inmobiliaria.objects.all()
    lookup_field = 'InmobiliariaID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            # permission_classes = [IsAuthenticated,
            #                       CheckAdminOrConsInmobPermission, ]
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, CheckAdminInmobPermission, ]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = Inmobiliaria.objects.filter(State=True)
        queryset = InmobiliariaSerializer.setup_eager_loading(queryset)
        serializer = InmobiliariaSerializer(
            queryset, many=True, context={
                'request': request})
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = CreateInmobiliariaSerializer(
            data=data, many=many, context={'request': request})

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response({"inmobiliaria": serializer.data,
                             "detail": "Inmobiliaria creada con éxito"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)

    def partial_update(self, request, InmobiliariaID):
        serializer = UpdateInmobiliariaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"inmobiliaria": serializer.data,
                             "detail": "Inmobiliaria modificada con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class ConstructoraViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = ConstructoraSerializer
    queryset = Constructora.objects.all()
    lookup_field = 'ConstructoraID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            # permission_classes = [IsAuthenticated,
            #                       CheckAdminOrConsInmobOrConsParamPermission, ]
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated,
                                  CheckAdminInmobOrAdminParamPermission, ]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = Constructora.objects.filter(State=True)
        serializer = ConstructoraSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = CreateConstructoraSerializer(
            data=data, many=many, context={'request': request})

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response({"constructora": serializer.data,
                             "detail": "Constructora creada con éxito"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)

    def partial_update(self, request, ConstructoraID):
        serializer = UpdateConstructoraSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"constructora": serializer.data,
                             "detail": "Constructora modificada con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class RegionViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RegionSerializer
    queryset = Region.objects.all()


class ProvinciaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProvinciaSerializer
    queryset = Provincia.objects.all()


class ComunaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ComunaSerializer
    queryset = Comuna.objects.all()


class ContactInfoTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactInfoTypeSerializer
    queryset = ContactInfoType.objects.all()


class UserInmobiliariaTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInmobiliariaTypeSerializer
    queryset = UserInmobiliariaType.objects.all()


class RepresentanteInmobiliariaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInmobiliariaSerializer

    def get_queryset(self):
        inmobiliaria_id = self.request.query_params.get('q', None)
        inmobiliaria = Inmobiliaria.objects.get(InmobiliariaID=inmobiliaria_id)
        user_inmobiliaria_type = UserInmobiliariaType.objects.get(
            Name=constants.USER_EMPRESA_TYPE[0])
        queryset = UserInmobiliaria.objects.filter(
            InmobiliariaID=inmobiliaria,
            UserInmobiliariaTypeID=user_inmobiliaria_type)

        return queryset


class AprobadorInmobiliariaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInmobiliariaSerializer

    def get_queryset(self):
        inmobiliaria_id = self.request.query_params.get('q', None)
        inmobiliaria = Inmobiliaria.objects.get(InmobiliariaID=inmobiliaria_id)
        user_inmobiliaria_type = UserInmobiliariaType.objects.get(
            Name=constants.USER_EMPRESA_TYPE[1])
        queryset = UserInmobiliaria.objects.filter(
            InmobiliariaID=inmobiliaria,
            UserInmobiliariaTypeID=user_inmobiliaria_type)

        return queryset


class UFNowAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UFSerializer

    def get(request, self):
        try:
            #date = datetime.datetime.now()
            #now = date.date()
            #uf = UF.objects.get(Date=now)
            uf = UF.objects.order_by('-Date').first()
			
            response = {
                'fecha': uf.Date,
                'valor': uf.Value
            }
            return Response(response, status=status.HTTP_200_OK)

        except(UF.DoesNotExist, ValidationError):
            return Response(
                {"detail": "El valor de la UF no está disponible en la fecha indicada o no se ha ingresado fecha."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UFAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UFSerializer

    def get(request, self, date):
        try:
            uf = UF.objects.get(Date=date)

            response = {
                'fecha': uf.Date,
                'valor': uf.Value
            }
            return Response(response, status=status.HTTP_200_OK)

        except(UF.DoesNotExist, ValidationError):
            return Response(
                {"detail": "El valor de la UF no está disponible en la fecha indicada o no se ha ingresado fecha."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConstantNumericViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ConstantNumericSerializer

    def list(self, request):
        name = self.request.query_params.get('q', None)
        constant = get_object_or_404(ConstantNumeric, Name__iexact=name)
        serializer = ConstantNumericSerializer(constant)
        return Response(serializer.data)
