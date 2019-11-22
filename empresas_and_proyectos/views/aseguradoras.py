from common.permissions import (
    CheckAdminParamPermission,
    CheckAdminOrConsParamPermission)
from empresas_and_proyectos.models.aseguradoras import Aseguradora
from empresas_and_proyectos.serializers.aseguradoras import AseguradoraSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class AseguradoraViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated, CheckAdminParamPermission,)
    serializer_class = AseguradoraSerializer
    queryset = Aseguradora.objects.all()
    lookup_field = 'AseguradoraID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            # permission_classes = [IsAuthenticated,
            #                       CheckAdminOrConsParamPermission, ]
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, CheckAdminParamPermission, ]
        return [permission() for permission in permission_classes]
