from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.permissions import (
    CheckAdminOrConsOrMoniProyectosPermission,
    CheckAdminOrVendedorOrMoniProyectosPermission,
    CheckAdminOrConsCliPermission,
    CheckAdminOrConsUsersPermission)
from common.services import download_pdf_views
from empresas_and_proyectos.models.proyectos import Proyecto
from users.models import User
from ventas.models.clientes import Cliente
from ventas.models.cotizaciones import (
    CotizacionType,
    Cotizacion)
from ventas.serializers.cotizaciones import (
    CotizacionTypeSerializer,
    CotizacionSerializer,
    DownloadCotizacionSerializer,
    CreateCotizacionSerializer)


class CotizacionTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CotizacionTypeSerializer
    queryset = CotizacionType.objects.all()


class CotizacionProyectoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        CheckAdminOrConsOrMoniProyectosPermission)
    serializer_class = CotizacionSerializer
    queryset = Cotizacion.objects.all()
    lookup_field = 'CotizacionID'

    def list(self, request):
        proyecto_id = self.request.query_params.get('q', None)
        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        queryset = Cotizacion.objects.filter(ProyectoID=proyecto)
        queryset = CotizacionSerializer.setup_eager_loading(queryset)
        serializer = CotizacionSerializer(queryset, many=True)

        return Response(serializer.data)


class DownloadCotizacionProyectoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DownloadCotizacionSerializer
    queryset = Cotizacion.objects.all()
    lookup_field = 'CotizacionID'

    def create(self, request):
        data = request.data
        serializer = DownloadCotizacionSerializer(data=data)

        if serializer.is_valid():
            cotizacion_id = serializer.validated_data.get("CotizacionID")
            letter_size = serializer.validated_data.get("LetterSize")
            response = HttpResponse(content_type='application/pdf')
            pdf = download_pdf_views(cotizacion_id, letter_size, response)
            response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % (
                pdf)
            return response
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class CotizacionViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CotizacionSerializer
    queryset = Cotizacion.objects.all()
    lookup_field = 'CotizacionID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated,
                                  CheckAdminOrConsOrMoniProyectosPermission, ]
        else:
            permission_classes = [
                IsAuthenticated,
                CheckAdminOrVendedorOrMoniProyectosPermission,
            ]
        return [permission() for permission in permission_classes]

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = CreateCotizacionSerializer(
            data=data, many=many, context={'request': request})

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"detail": "Cotización creada con éxito",
                             "cotizacion": CotizacionSerializer(instance).data},
                            status=status.HTTP_201_CREATED)

        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)


class CotizacionesClienteViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminOrConsCliPermission)
    serializer_class = CotizacionSerializer
    queryset = Cotizacion.objects.all()
    lookup_field = 'CotizacionID'

    def list(self, request):
        cliente_id = self.request.query_params.get('q', None)
        cliente = Cliente.objects.get(UserID=cliente_id)
        queryset = Cotizacion.objects.filter(ClienteID=cliente)
        queryset = CotizacionSerializer.setup_eager_loading(queryset)
        serializer = CotizacionSerializer(queryset, many=True)

        return Response(serializer.data)


class CotizacionesCotizadorViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminOrConsUsersPermission)
    serializer_class = CotizacionSerializer
    queryset = Cotizacion.objects.all()
    lookup_field = 'CotizacionID'

    def list(self, request):
        cotizador_id = self.request.query_params.get('q', None)
        cotizador = User.objects.get(UserID=cotizador_id)
        queryset = Cotizacion.objects.filter(CotizadorID=cotizador)
        queryset = CotizacionSerializer.setup_eager_loading(queryset)
        serializer = CotizacionSerializer(queryset, many=True)

        return Response(serializer.data)
