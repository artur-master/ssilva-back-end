from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common import constants
from empresas_and_proyectos.models.proyectos import Proyecto
from ventas.models.promesas import Promesa
from ventas.serializers.desistimiento import (
    RegisterDesistimientoSerializer,
    UploadConfeccionDesistimientoSerializer,
    RgisterRefundSerializer)


class RegisterDesistimientoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterDesistimientoSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = RegisterDesistimientoSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )
        if serializer.is_valid():
            instance = serializer.save()
            return Response({"promesa": RegisterDesistimientoSerializer(instance, context={'request': request}).data,
                             "detail": "Register desistimiento con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class UploadConfeccionDesistimientoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UploadConfeccionDesistimientoSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = UploadConfeccionDesistimientoSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"detail": "Documentos subidos con éxito",
                             "promesa": UploadConfeccionDesistimientoSerializer(instance).data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class RegisterRefundViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RgisterRefundSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = RgisterRefundSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )
        if serializer.is_valid():
            instance = serializer.save()
            return Response({"promesa": RgisterRefundSerializer(instance, context={'request': request}).data,
                             "detail": "Devolución garantía con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)
