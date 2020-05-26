from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from empresas_and_proyectos.models.proyectos import Proyecto
from common.notifications import (
    eliminar_notificacion_reserva_rechazada,
    eliminar_notificacion_reserva_cancelada)
from common.permissions import (
    CheckAdminOrVendedorOrMoniOrConsProyectosPermission,
    CheckVendedorPermission,
    CheckAdminOrVendedorOrMoniProyectosPermission,
    CheckAsistenteComercialPermission)
from common.services import download_pre_approbation_views
from ventas.models.reservas import Reserva
from ventas.serializers.reservas import (
    RetrieveReservaSerializer,
    ListReservaSerializer,
    CreateReservaSerializer,
    UpdateReservaSerializer,
    SendControlReservaSerializer,
    ControlReservaSerializer,
    CancelReservaSerializer,
    UploadDocumentsReservaSerializer,
    DownloadPreApprobationSerializer
)
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ventas.serializers.documents_venta import DocumentVentaSerializer


class ReservaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RetrieveReservaSerializer
    queryset = Reserva.objects.all()
    lookup_field = 'ReservaID'

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.action == 'retrieve' or self.action == 'list':
    #         permission_classes = [IsAuthenticated, CheckAdminOrVendedorOrMoniOrConsProyectosPermission, ]
    #     elif self.action == 'create':
    #         permission_classes = [IsAuthenticated,
    #                               CheckVendedorPermission, ]
    #     elif self.action == 'partial_update':
    #         permission_classes = [IsAuthenticated,
    #                               CheckAdminOrVendedorOrMoniProyectosPermission, ]
    #     else:
    #         permission_classes = [IsAuthenticated, ]
    #     return [permission() for permission in permission_classes]

    def list(self, request):
        proyecto_id = self.request.query_params.get('q', None)
        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        queryset = Reserva.objects.filter(ProyectoID=proyecto)
        queryset = ListReservaSerializer.setup_eager_loading(queryset)
        serializer = ListReservaSerializer(queryset, context={'request': request}, many=True)

        return Response(serializer.data)

    def retrieve(self, request, ReservaID):
        queryset = Reserva.objects.all()
        queryset = RetrieveReservaSerializer.setup_eager_loading(queryset)
        instance = get_object_or_404(queryset, ReservaID=ReservaID)
        current_user = request.user
        eliminar_notificacion_reserva_rechazada(instance, current_user)
        eliminar_notificacion_reserva_cancelada(instance, current_user)
        serializer = RetrieveReservaSerializer(
            instance, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        
        serializer = CreateReservaSerializer(data=data, many=many, context={'request': request})

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"detail": "Reserva creada con éxito",
                             "reserva": RetrieveReservaSerializer(instance, context={'request': request}).data},
                            status=status.HTTP_201_CREATED)
        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)

    def partial_update(self, request, ReservaID):
        serializer = UpdateReservaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"reserva": RetrieveReservaSerializer(instance, context={'request': request}).data,
                             "detail": "Reserva modificada con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class SendControlReservaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminOrVendedorOrMoniProyectosPermission)
    serializer_class = SendControlReservaSerializer
    queryset = Reserva.objects.all()
    lookup_field = 'ReservaID'

    def partial_update(self, request, ReservaID):
        serializer = SendControlReservaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"reserva": RetrieveReservaSerializer(instance, context={'request': request}).data,
                             "detail": "Reserva enviada a control con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class ApproveControlReservaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAsistenteComercialPermission)
    serializer_class = ControlReservaSerializer
    queryset = Reserva.objects.all()
    lookup_field = 'ReservaID'

    def partial_update(self, request, ReservaID):
        serializer = ControlReservaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            resolution = serializer.validated_data.get("Resolution")
            if resolution:
                instance = serializer.save()
                return Response({"reserva": RetrieveReservaSerializer(instance, context={'request': request}).data,
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


class CancelReservaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminOrVendedorOrMoniProyectosPermission)
    serializer_class = CancelReservaSerializer
    queryset = Reserva.objects.all()
    lookup_field = 'ReservaID'

    def partial_update(self, request, ReservaID):
        serializer = CancelReservaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"reserva": RetrieveReservaSerializer(instance, context={'request': request}).data,
                             "detail": "Reserva cancelada con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class UploadDocumentsReservaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminOrVendedorOrMoniProyectosPermission)
    serializer_class = UploadDocumentsReservaSerializer
    queryset = Reserva.objects.all()
    lookup_field = 'ReservaID'

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = UploadDocumentsReservaSerializer(
            data=data, many=many, context={'request': request})

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"detail": "Documentos subidos con éxito",
                             "Documentos": DocumentVentaSerializer(instance,context={'url': request}).data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class DownloadPreApprobationViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DownloadPreApprobationSerializer
    queryset = Reserva.objects.all()
    lookup_field = 'ReservaID'

    def create(self, request):
        data = request.data
        serializer = DownloadPreApprobationSerializer(data=data)

        if serializer.is_valid():
            reserva_id = serializer.validated_data.get("ReservaID")
            letter_size = serializer.validated_data.get("LetterSize")
            response = HttpResponse(content_type='application/pdf')
            pdf = download_pre_approbation_views(reserva_id, letter_size, response)
            response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % (
                pdf)
            return response
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)
