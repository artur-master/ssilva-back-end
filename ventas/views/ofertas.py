from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from common import constants
from common.permissions import (
    CheckAdminOrVendedorOrMoniOrConsProyectosPermission,
    CheckAdminOrVendedorOrMoniProyectosPermission,
    CheckAdminMoniProyectosPermission,
    CheckAprobadorPermission,
    CheckApproveUpdateOfertaPermission,
    CheckRecepcionaGarantiasPermission,
    CheckAsistenteComercialPermission,
    CheckApproveConfeccionPromesaPermission)
from empresas_and_proyectos.models.proyectos import Proyecto
from ventas.models.ofertas import Oferta
from ventas.models.payment_forms import PreAprobacionCredito
from ventas.serializers.ofertas import (
    RetrieveOfertaSerializer,
    ListOfertaSerializer,
    UpdateOfertaSerializer,
    SendApproveInmobiliariaSerializer,
    ApproveInmobiliariaSerializer,
    RegisterReceptionGuaranteeSerializer,
    RegisterInstitucionFinancieraSerializer,
    ListPreAprobacionCreditoSerializer,
    RegisterResultPreAprobacionSerializer,
    ApproveConfeccionPromesaSerializer,
    ApproveUpdateOfertaSerializer,
    CancelOfertaSerializer,
    WithdrawOfertaSerializer)


class OfertaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RetrieveOfertaSerializer
    queryset = Oferta.objects.all()
    lookup_field = 'OfertaID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [IsAuthenticated, CheckAdminOrVendedorOrMoniOrConsProyectosPermission]
        else:
            permission_classes = [IsAuthenticated,
                                  CheckAdminOrVendedorOrMoniProyectosPermission, ]

        return [permission() for permission in permission_classes]

    def list(self, request):
        proyecto_id = self.request.query_params.get('q', None)
        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        queryset = Oferta.objects.filter(ProyectoID=proyecto).exclude(OfertaState__in=[constants.OFERTA_STATE[5]])
        queryset = ListOfertaSerializer.setup_eager_loading(queryset)
        serializer = ListOfertaSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, OfertaID):
        queryset = Oferta.objects.all()
        queryset = RetrieveOfertaSerializer.setup_eager_loading(queryset)
        instance = get_object_or_404(queryset, OfertaID=OfertaID)

        serializer = RetrieveOfertaSerializer(
            instance, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, OfertaID):
        serializer = UpdateOfertaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"detail": "Oferta modificada con éxito",
                             "oferta": RetrieveOfertaSerializer(instance=instance, context={'request': request}).data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class SendOfertaApproveInmobiliariaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminMoniProyectosPermission)
    serializer_class = SendApproveInmobiliariaSerializer
    queryset = Oferta.objects.all()
    lookup_field = 'OfertaID'

    def partial_update(self, request, OfertaID):
        serializer = SendApproveInmobiliariaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"oferta": serializer.data,
                             "detail": "Oferta enviada con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class ApproveInmobiliariaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAprobadorPermission)
    serializer_class = ApproveInmobiliariaSerializer
    queryset = Oferta.objects.all()
    lookup_field = 'OfertaID'

    def partial_update(self, request, OfertaID):
        serializer = ApproveInmobiliariaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            resolution = serializer.validated_data.get("Resolution")
            if resolution:
                serializer.save()
                return Response({"reserva": serializer.data,
                                 "detail": "Aprobación realizada con éxito"},
                                status=status.HTTP_200_OK)
            else:
                serializer.save()
                return Response({"reserva": serializer.data,
                                 "detail": "Rechazo realizado con éxito"},
                                status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class RegisterReceptionGuaranteeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckRecepcionaGarantiasPermission)
    serializer_class = RegisterReceptionGuaranteeSerializer
    queryset = Oferta.objects.all()
    lookup_field = 'OfertaID'

    def partial_update(self, request, OfertaID):
        serializer = RegisterReceptionGuaranteeSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"oferta": serializer.data,
                             "detail": "Recepción registrada con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class RegisterInstitucionFinancieraViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAsistenteComercialPermission)
    serializer_class = RegisterInstitucionFinancieraSerializer
    queryset = PreAprobacionCredito.objects.all()
    lookup_field = 'PreAprobacionCreditoID'

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = RegisterInstitucionFinancieraSerializer(
            data=data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Instituciones Financieras agregadas con éxito",
                             "InstitucionFinancieras": serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class ListPreAprobacionCreditoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ListPreAprobacionCreditoSerializer
    queryset = PreAprobacionCredito.objects.all()
    lookup_field = 'PreAprobacionCreditoID'

    def list(self, request):
        oferta_id = self.request.query_params.get('q', None)
        oferta = Oferta.objects.get(OfertaID=oferta_id)
        queryset = PreAprobacionCredito.objects.filter(OfertaID=oferta)
        serializer = ListPreAprobacionCreditoSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)


class RegisterResultPreAprobacionViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAsistenteComercialPermission)
    serializer_class = RegisterResultPreAprobacionSerializer
    queryset = Oferta.objects.all()
    lookup_field = 'OfertaID'

    def partial_update(self, request, OfertaID):
        serializer = RegisterResultPreAprobacionSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"oferta": serializer.data,
                             "detail": "Resultado pre aprobación ingresado con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class ApproveConfeccionPromesaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckApproveConfeccionPromesaPermission)
    serializer_class = ApproveConfeccionPromesaSerializer
    queryset = Oferta.objects.all()
    lookup_field = 'OfertaID'

    def partial_update(self, request, OfertaID):
        serializer = ApproveConfeccionPromesaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            resolution = serializer.validated_data.get("Resolution")
            if resolution:
                serializer.save()
                return Response({"oferta": serializer.data,
                                 "detail": "Aprobación realizada con éxito"},
                                status=status.HTTP_200_OK)
            else:
                serializer.save()
                return Response({"oferta": serializer.data,
                                 "detail": "Rechazo realizado con éxito"},
                                status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class ApproveUpdateOfertaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckApproveUpdateOfertaPermission)
    serializer_class = ApproveUpdateOfertaSerializer
    queryset = Oferta.objects.all()
    lookup_field = 'OfertaID'

    def partial_update(self, request, OfertaID):
        serializer = ApproveUpdateOfertaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            resolution = serializer.validated_data.get("Resolution")
            if resolution:
                serializer.save()
                return Response({"oferta": serializer.data,
                                 "detail": "Aprobación modificaciones oferta"},
                                status=status.HTTP_200_OK)
            else:
                serializer.save()
                return Response({"oferta": serializer.data,
                                 "detail": "Rechazo modificaciones oferta"},
                                status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class CancelOfertaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminOrVendedorOrMoniProyectosPermission)
    serializer_class = CancelOfertaSerializer
    queryset = Oferta.objects.all()
    lookup_field = 'OfertaID'

    def partial_update(self, request, OfertaID):
        serializer = CancelOfertaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"oferta": serializer.data,
                             "detail": "Oferta cancelada con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class WithdrawOfertaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminMoniProyectosPermission)
    serializer_class = WithdrawOfertaSerializer
    queryset = Oferta.objects.all()
    lookup_field = 'OfertaID'

    def partial_update(self, request, OfertaID):
        serializer = WithdrawOfertaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"oferta": serializer.data,
                             "detail": "Oferta desistimien con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)
