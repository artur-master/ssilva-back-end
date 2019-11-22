from django.shortcuts import get_object_or_404
from common.permissions import (
    CheckAdminMoniOrConsProyectosPermission,
    CheckAdminOrConsParamPermission,
    CheckAdminParamPermission)
from empresas_and_proyectos.models.proyectos import Proyecto
from empresas_and_proyectos.models.proyectos_logs import (
    ProyectoLog,
    ProyectoLogType)
from empresas_and_proyectos.serializers.proyectos import (
    ProyectoLogPDFSerializer,
    ProyectoLogTypeSerializer,
    UpdateProyectoLogTypeSerializer)
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ProyectoLogViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (
    #     IsAuthenticated,
    #     CheckAdminMoniOrConsProyectosPermission)
    serializer_class = ProyectoLogPDFSerializer
    queryset = ProyectoLog.objects.all()
    lookup_field = 'ProyectoLogID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, CheckAdminMoniOrConsProyectosPermission]
        return [permission() for permission in permission_classes]

    def list(self, request):
        proyecto_id = self.request.query_params.get('q', None)
        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        queryset = ProyectoLog.objects.filter(
            ProyectoID=proyecto
        )
        queryset = ProyectoLogPDFSerializer.setup_eager_loading(queryset)
        serializer = ProyectoLogPDFSerializer(
            queryset, many=True, context={
                'request': request})

        return Response(serializer.data)

    def retrieve(self, request, ProyectoLogID):
        queryset = ProyectoLog.objects.all()
        queryset = ProyectoLogPDFSerializer.setup_eager_loading(queryset)
        instance = get_object_or_404(queryset, ProyectoLogID=ProyectoLogID)

        serializer = ProyectoLogPDFSerializer(
            instance, context={'request': request})
        return Response(serializer.data)


class ProyectoLogTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProyectoLogTypeSerializer
    queryset = ProyectoLogType.objects.all()
    lookup_field = 'ProyectoLogTypeID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [IsAuthenticated,
                                  CheckAdminOrConsParamPermission, ]
        if self.action == 'create':
            permission_classes = [IsAuthenticated, CheckAdminParamPermission, ]
        if self.action == 'partial_update':
            permission_classes = [IsAuthenticated, CheckAdminParamPermission, ]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, ProyectoLogTypeID):
        serializer = UpdateProyectoLogTypeSerializer(
            self.get_object(), data=request.data,
            partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Máximo de días modificado con éxito",
                             "proyecto_log_type": serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)