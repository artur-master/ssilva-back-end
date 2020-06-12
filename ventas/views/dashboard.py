from ventas.models.ventas_logs import VentaLog
from users.models import User
from users.serializers.users import ListResponsableSerializer
from ventas.models.reservas import Reserva
from ventas.models.promesas import Promesa
from ventas.models.cotizaciones import Cotizacion
from ventas.models.ofertas import Oferta
from ventas.serializers.ventas_logs import VentaLogUserSerializer
from ventas.serializers.reservas import ListReservaActionSerializer
from ventas.serializers.cotizaciones import ListCotizacionActionSerializer
from ventas.serializers.ofertas import ListOfertaActionSerializer
from ventas.serializers.promesas import ListPromesaActionSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from common import constants

class PendingActionsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = VentaLogUserSerializer
    queryset = VentaLog.objects.all()
    
    def get_data(self, ActionSerializer, queryset):
        queryset = ActionSerializer.setup_eager_loading(queryset)
        serializer = ActionSerializer(queryset, many=True)
        return serializer.data

    def list(self, request):
        # cotizacion_data = Cotizacion.objects.all()
        # cotizacion_queryset = cotizacion_data.filter(CotizacionStateID__Name=constants.COTIZATION_STATE[0])
        # cotizationAction = self.get_data(ListCotizacionActionSerializer, cotizacion_queryset)

        reserva_data = Reserva.objects.all()
        reserva_pending_data = reserva_data.exclude(
            ReservaStateID__Name='Oferta')     
        reserva_queryset = reserva_data.filter(
            ReservaStateID__Name__in=[constants.RESERVA_STATE[0], constants.RESERVA_STATE[1]])
        reservaAction = self.get_data(ListReservaActionSerializer, reserva_queryset)

        oferta_data = Oferta.objects.all()
        oferta_pending_data = oferta_data.exclude(OfertaState='Promesa')
        oferta_queryset = oferta_data.filter(
            OfertaState__in=[constants.OFERTA_STATE[0], constants.OFERTA_STATE[1]])
        oferta_serializer = ListOfertaActionSerializer(oferta_queryset, many=True)

        promesa_data = Promesa.objects.all()
        promesa_pending_data = promesa_data.exclude(
            PromesaState='Pendiente firma inmobiliaria')
        promesa_queryset = promesa_data.filter(
            PromesaState__in=[
                constants.PROMESA_STATE[0], 
                constants.PROMESA_STATE[9], 
                constants.PROMESA_STATE[11],
                constants.PROMESA_STATE[13]]
        )
        promesa_serializer = ListPromesaActionSerializer(promesa_queryset, many=True)
        
        counter = [("Reservas" , {'total': reserva_data.count(),
                                  'Pending': reserva_pending_data.count()}),
                   ("Ofertas", {'total': oferta_data.count(),
                                'Pending': oferta_pending_data.count()}),
                   ("Promesas", {'total': promesa_data.count(),
                                 'Pending': promesa_pending_data.count()}),
                   ("Escrituras", {'total': oferta_data.count(),
                                  'Pending': oferta_pending_data.count()})]
        
        PendingActions = dict(Reserva=reservaAction,
                              Ofertas=oferta_serializer.data,
                              Promesa=promesa_serializer.data)
        
        return Response({"count": counter, "PendingAction": PendingActions})


class AllUserViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ListResponsableSerializer
    queryset = User.objects.all()

class AllLogsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = VentaLogUserSerializer
    log_queryset = VentaLog.objects.all().order_by('-Date')
    queryset = VentaLogUserSerializer.setup_eager_loading(log_queryset)
