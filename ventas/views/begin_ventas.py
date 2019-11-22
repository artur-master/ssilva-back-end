from empresas_and_proyectos.models.etapas import Etapa
from common.permissions import CheckAdminMoniProyectosPermission
from empresas_and_proyectos.serializers.etapas import BeginVentaSerializer
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class BeginVentaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminMoniProyectosPermission)
    serializer_class = BeginVentaSerializer
    queryset = Etapa.objects.all()
    lookup_field = 'EtapaID'

    def partial_update(self, request, EtapaID):
        serializer = BeginVentaSerializer(
            self.get_object(), data=request.data, partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Proceso de ventas comenzado"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)