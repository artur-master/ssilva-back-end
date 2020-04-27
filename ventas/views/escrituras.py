from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, APIException

from common.permissions import (
    CheckAdminOrConsOrMoniProyectosPermission,
    CheckAdminOrVendedorOrMoniProyectosPermission,
    CheckAdminOrConsCliPermission,
    CheckAdminOrConsUsersPermission)
from common.services import download_pdf_views
from empresas_and_proyectos.models.proyectos import Proyecto
from users.models import User

from ventas.models.escrituras import Escritura
from ventas.serializers.escrituras import (
    EscrituraSerializer,ListEscrituraSerializer, UpdateEscrituraSerializer,
    ConfirmProyectoSerializer, UpdateProyectoSerializer)
from empresas_and_proyectos.serializers.proyectos import (
    ProyectoSerializer, 
    RetrieveProyectoSerializer)

class EscrituraViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = EscrituraSerializer
    queryset = Escritura.objects.all()
    lookup_field = 'EscrituraID'

    # def get_permissions(self):
    #     if self.action == 'retrieve' or self.action == 'list':
    #         permission_classes = [IsAuthenticated, ]
    #     if self.action == 'create':
    #         permission_classes = [IsAuthenticated, ]
    #     if self.action == 'partial_update':
    #         permission_classes = [IsAuthenticated, ]
    #     return [permission() for permission in permission_classes]

    # def retrieve(self, request, EscrituraID):
    #     queryset = Escritura.objects.all()
    #     queryset = EscrituraSerializer.setup_eager_loading(queryset)
    #     instance = get_object_or_404(queryset, EscrituraID=EscrituraID)

    #     serializer = EscrituraSerializer(
    #         instance, context={'request': request})

    #     return Response(serializer.data)

    def list(self, request):
        proyecto_id = self.request.query_params.get('q', None)
        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        queryset = Escritura.objects.filter(ProyectoID=proyecto)
        # queryset = EscrituraSerializer.setup_eager_loading(queryset)
        # serializer = EscrituraSerializer(queryset, context={'request': request}, many=True)

        queryset = ListEscrituraSerializer.setup_eager_loading(queryset)
        serializer = ListEscrituraSerializer(queryset, context={'request': request}, many=True)

        return Response(serializer.data)

    def partial_update(self, request, EscrituraID):
        serializer = UpdateEscrituraSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )
        
        if serializer.is_valid():
            instance = serializer.save()
            # escritura = self.get_object()
            
            return Response({"escritura": EscrituraSerializer(instance, context={'request': request}).data,
                             "detail": "message"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class EscrituraProyectoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProyectoSerializer
    queryset = Proyecto.objects.all()
    lookup_field = 'ProyectoID'

    def partial_update(self, request, ProyectoID):
        serializer = UpdateProyectoSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )
        if serializer.is_valid():
            instance = serializer.save()
            retrieve_serializer = RetrieveProyectoSerializer(instance, context={'request': request})
            return Response({"proyecto": retrieve_serializer.data,
                             "detail": "Proyecto confirmado con éxito."},
                            status=status.HTTP_200_OK)
        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)

        
    @action(detail=True, methods=['patch'])
    def confirm_escritura(self, request, ProyectoID):
        proyecto = Proyecto.objects.get(ProyectoID=ProyectoID)
        # queryset = Escritura.objects.filter(ProyectoID=proyecto)
        
        serializer = ConfirmProyectoSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            retrieve_serializer = RetrieveProyectoSerializer(instance, context={'request': request})
            return Response({"proyecto": retrieve_serializer.data,
                            "detail": "Proyecto actualizado con éxito."},
                            status=status.HTTP_200_OK)
        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)