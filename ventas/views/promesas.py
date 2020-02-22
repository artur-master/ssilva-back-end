from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common import constants
from common.permissions import (
    CheckUploadFirmaDocumentPromesaPermission,
    CheckAdminOrVendedorOrMoniProyectosPermission,
    CheckConfeccionaMaquetasPromesaPermission)
from empresas_and_proyectos.models.proyectos import Proyecto
from ventas.models.promesas import Promesa
from ventas.serializers.promesas import (
    ListPromesaSerializer,
    RetrievePromesaSerializer,
    ApproveMaquetaPromesaSerializer,
    ControlPromesaSerializer,
    RegisterSendPromesaToInmobiliariaSerializer,
    GenerateFacturaSerializer,
    RegisterSignatureInmobiliariaSerializer,
    LegalizePromesaSerializer,
    SendCopiesSerializer,
    UpdatePromesaSerializer,
    UploadConfeccionPromesaSerializer,
    UploadFirmaDocumentSerializer,
    SendNegociacionJPSerializer,
    SendNegociacionINSerializer,
    ControlNegociacionSerializer, SendPromesaToClientSerializer)


class PromesaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ListPromesaSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        if self.action == 'create':
            permission_classes = [IsAuthenticated, ]
        if self.action == 'partial_update':
            permission_classes = [IsAuthenticated, ]
        return [permission() for permission in permission_classes]

    def list(self, request):
        proyecto_id = self.request.query_params.get('q', None)
        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        queryset = Promesa.objects.filter(ProyectoID=proyecto, IsOfficial=True)
        queryset = ListPromesaSerializer.setup_eager_loading(queryset)
        serializer = ListPromesaSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, PromesaID):
        queryset = Promesa.objects.all()
        queryset = RetrievePromesaSerializer.setup_eager_loading(queryset)
        instance = get_object_or_404(queryset, PromesaID=PromesaID)
        # current_user = request.user
        serializer = RetrievePromesaSerializer(
            instance, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, PromesaID):
        serializer = UpdatePromesaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            promesa = self.get_object()
            if (promesa.PromesaState == constants.PROMESA_STATE[0] or
                    promesa.PromesaState == constants.PROMESA_STATE[1] or
                    promesa.PromesaState == constants.PROMESA_STATE[9]):

                message = "Modificación realizada con éxito, dirijase a modificar Oferta {folio} para continuar el " \
                          "flujo".format(folio=promesa.Folio)
                promesa.delete()
            else:
                message = "Modificación realizada con éxito, en espera de aprobación ".format(folio=promesa.Folio)
            return Response({"promesa": RetrievePromesaSerializer(instance).data,
                             "detail": message},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class UploadConfeccionPromesaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckConfeccionaMaquetasPromesaPermission)
    serializer_class = UploadConfeccionPromesaSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = UploadConfeccionPromesaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"detail": "Documentos subidos con éxito",
                             "promesa": UploadConfeccionPromesaSerializer(instance).data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class ApproveMaquetaPromesaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ApproveMaquetaPromesaSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = ApproveMaquetaPromesaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            resolution = serializer.validated_data.get("Resolution")
            instance = serializer.save()
            if resolution:
                return Response({"promesa": RetrievePromesaSerializer(instance, context={'request': request}).data,
                                 "detail": "Aprobación realizada con éxito"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"promesa": RetrievePromesaSerializer(instance, context={'request': request}).data,
                                 "detail": "Rechazo realizado con éxito"},
                                status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class UploadFirmaDocumentViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckUploadFirmaDocumentPromesaPermission)
    serializer_class = UploadFirmaDocumentSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = UploadFirmaDocumentSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"detail": "Documentos subidos con éxito",
                             "promesa": UploadFirmaDocumentSerializer(instance).data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class ApproveControlPromesaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ControlPromesaSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = ControlPromesaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            resolution = serializer.validated_data.get("Resolution")
            instance = serializer.save()
            if resolution:
                return Response({"promesa": RetrievePromesaSerializer(instance, context={'request': request}).data,
                                 "detail": "Aprobación realizada con éxito"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"promesa": RetrievePromesaSerializer(instance, context={'request': request}).data,
                                 "detail": "Rechazo realizado con éxito"},
                                status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class RegisterSendPromesaToInmobiliariaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSendPromesaToInmobiliariaSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = RegisterSendPromesaToInmobiliariaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"promesa": RetrievePromesaSerializer(instance, context={'request': request}).data,
                             "detail": "Envio promesa a inmobiliaria con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class GenerateFacturaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = GenerateFacturaSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = GenerateFacturaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"promesa": RetrievePromesaSerializer(instance, context={'request': request}).data,
                             "detail": "Generar factura con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class RegisterSignatureInmobiliariaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSignatureInmobiliariaSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = RegisterSignatureInmobiliariaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"promesa": RetrievePromesaSerializer(instance, context={'request': request}).data,
                             "detail": "Registro firma de inmobiliaria con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class LegalizePromesaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = LegalizePromesaSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = LegalizePromesaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"promesa": RetrievePromesaSerializer(instance, context={'request': request}).data,
                             "detail": "Registro de fecha de legalización con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class SendCopiesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SendCopiesSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = SendCopiesSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"promesa": RetrievePromesaSerializer(instance, context={'request': request}).data,
                             "detail": "Registro envio de copias con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class NegociacionPromesaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SendNegociacionJPSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = SendNegociacionJPSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"promesa": RetrievePromesaSerializer(instance, context={'request': request}).data,
                             "detail": "Envio negociación a JP"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class SendNegociacionPromesaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SendNegociacionINSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = SendNegociacionINSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"promesa": RetrievePromesaSerializer(instance, context={'request': request}).data,
                             "detail": "Envio negociación a IN"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class ControlNegociacionPromesaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ControlNegociacionSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = ControlNegociacionSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )
        if serializer.is_valid():
            resolution = serializer.validated_data.get("Resolution")
            if resolution:
                instance = serializer.save()
                return Response({"promesa": RetrievePromesaSerializer(instance, context={'request': request}).data,
                                 "detail": "Aprobación negociación con éxito"},
                                status=status.HTTP_200_OK)
            else:
                instance = serializer.save()
                return Response({"promesa": RetrievePromesaSerializer(instance, context={'request': request}).data,
                                 "detail": "Rechazo negociación con éxito"},
                                status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class SendPromesaToClientViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SendPromesaToClientSerializer
    queryset = Promesa.objects.all()
    lookup_field = 'PromesaID'

    def partial_update(self, request, PromesaID):
        serializer = SendPromesaToClientSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"promesa": RetrievePromesaSerializer(instance, context={'request': request}).data,
                             "detail": "Envio promesa a cliente con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)
