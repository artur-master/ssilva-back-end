from ventas.models.clientes import Cliente
from ventas.models.ventas_logs import VentaLog
from users.models import User
from ventas.models.reservas import Reserva
from ventas.models.promesas import Promesa
from ventas.models.cotizaciones import Cotizacion
from ventas.models.ofertas import Oferta
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

    def get_state(self, IDS, Id):
        for res_id in IDS:
            if ([(Id == str(o)) for o in res_id.values()][0]):
                return True
        return False
    
    def list(self, request):
        cliente_id = self.request.query_params.get('q', None)
        cotizador = User.objects.get(UserID=cliente_id)
        queryset = VentaLog.objects.filter(UserID=request.user.id, ClienteID=cotizador)
        queryset = VentaLogVendedorSerializer.setup_eager_loading(queryset)
        serializer = VentaLogVendedorSerializer(queryset, many=True)
        Reservas = list(Reserva.objects.values('ReservaID'))
        Ofertas = list(Oferta.objects.values('OfertaID'))
        Cotizaciones = list(Cotizacion.objects.values('CotizacionID'))
        Promesas = list(Promesa.objects.values('PromesaID'))
        datas = []
        for data in serializer.data:
            ventaId = list(data.values())[1]
            if(self.get_state(Reservas, ventaId)):
                data["state"] = "Reserva"
                data["dis_state"] = "Reserva"
            elif (self.get_state(Ofertas, ventaId)):
                data["state"] = "Oferta"
                data["dis_state"] = "Oferta"
            elif (self.get_state(Cotizaciones, ventaId)):
                data["state"] = "Cotizacion"
                data["dis_state"] = "Cotización"
            elif (self.get_state(Promesas, ventaId)):
                data["state"] = "Promesa"
                data["dis_state"] = "Promesa"
            else:
                continue

            datas.append(data)                 

        return Response(datas)


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
