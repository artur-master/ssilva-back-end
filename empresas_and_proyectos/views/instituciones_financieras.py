from common.permissions import (
    CheckAdminParamPermission,
    CheckAdminOrConsParamPermission)
from empresas_and_proyectos.models.instituciones_financieras import (
    InstitucionFinanciera)
from empresas_and_proyectos.serializers.instituciones_financieras import (
    InstitucionFinancieraSerializer)
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class InstitucionFinancieraViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminParamPermission,)
    serializer_class = InstitucionFinancieraSerializer
    queryset = InstitucionFinanciera.objects.all()
    lookup_field = 'InstitucionFinancieraID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [IsAuthenticated,
                                  CheckAdminOrConsParamPermission, ]
        else:
            permission_classes = [IsAuthenticated, CheckAdminParamPermission, ]
        return [permission() for permission in permission_classes]

