from ventas.models.clientes import Cliente
from ventas.models.ventas_logs import VentaLog
from users.models import User
from ventas.serializers.ventas_logs import VentaLogClienteSerializer, VentaLogVendedorSerializer, VentaLogSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class VentaLogClienteViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = VentaLogClienteSerializer
    queryset = VentaLog.objects.all()
    lookup_field = 'ClienteID'

    def list(self, request):
        cliente_id = self.request.query_params.get('q', None)
        cliente = Cliente.objects.get(UserID=cliente_id)
        queryset = VentaLog.objects.filter(ClienteID=cliente)
        queryset = VentaLogClienteSerializer.setup_eager_loading(queryset)
        serializer = VentaLogClienteSerializer(queryset, many=True)

        return Response(serializer.data)


class VentaLogVendedorViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = VentaLogVendedorSerializer
    queryset = VentaLog.objects.all()
    lookup_field = 'UserID'

    def list(self, request):
        cliente_id = self.request.query_params.get('q', None)
        cotizador = User.objects.get(UserID=cliente_id)
        queryset = VentaLog.objects.filter(UserID=cotizador)
        queryset = VentaLogVendedorSerializer.setup_eager_loading(queryset)
        serializer = VentaLogVendedorSerializer(queryset, many=True)

        return Response(serializer.data)


class VentaLogViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = VentaLogSerializer
    queryset = VentaLog.objects.all()
    lookup_field = 'Folio'

    def list(self, request):
        folio = self.request.query_params.get('q', None)
        queryset = VentaLog.objects.filter(Folio=folio)
        queryset = VentaLogSerializer.setup_eager_loading(queryset)
        serializer = VentaLogSerializer(queryset, many=True)

        return Response(serializer.data)
