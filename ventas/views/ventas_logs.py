from ventas.models.clientes import Cliente
from ventas.models.ventas_logs import VentaLog, UserSummary
from users.models import User
from ventas.models.reservas import Reserva
from ventas.models.promesas import Promesa
from ventas.models.cotizaciones import Cotizacion
from ventas.models.ofertas import Oferta
from ventas.serializers.ventas_logs import VentaLogClienteSerializer, VentaLogVendedorSerializer, VentaLogSerializer, VentaLogUserSerializer, UserSummarySerializer
from ventas.serializers.reservas import ListReservaSerializer, ListReservaActionSerializer
from ventas.serializers.cotizaciones import ListCotizacionActionSerializer
from ventas.serializers.ofertas import ListOfertaActionSerializer
from ventas.serializers.promesas import ListPromesaActionSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from common import constants

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
                data["dis_state"] = "Cotizacion"
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

class VentaLogUserViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = VentaLogSerializer
    queryset = VentaLog.objects.all()
    
    def get_data(self, ActionSerializer, queryset):
        queryset = ActionSerializer.setup_eager_loading(queryset)
        serializer = ActionSerializer(queryset, many=True)
        return serializer.data

    def list(self, request):
        log_queryset = VentaLog.objects.all().order_by('-Date')
        queryset = VentaLogUserSerializer.setup_eager_loading(log_queryset)
        log_serializer = VentaLogUserSerializer(queryset, many=True)

        cotizacion_data = Cotizacion.objects.all()
        cotizacion_queryset = cotizacion_data.filter(CotizacionStateID__Name=constants.COTIZATION_STATE[0])
        cotizationAction = self.get_data(ListCotizacionActionSerializer, cotizacion_queryset)

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
        
        PendingActions = dict(Cotizacion=cotizationAction,
                              Reserva=reservaAction,
                              Ofertas=oferta_serializer.data,
                              Promesa=promesa_serializer.data)
        
        return Response({"logs": log_serializer.data, 
                         "count": counter, 
                         "PendingAction": PendingActions,
                        })


class UserSummaryViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = VentaLogSerializer
    queryset = VentaLog.objects.all()

    def get_data(self, ActionSerializer, queryset):
        queryset = ActionSerializer.setup_eager_loading(queryset)
        serializer = ActionSerializer(queryset, many=True)
        return serializer.data

    def list(self, request):
        users = User.objects.all()
        serializer = UserSummarySerializer(users, many=True)
        for user in serializer.data:
            user_id = user['id']
            nombre = user['Nombre']
            tipos = user['Tipo']
            tipo_field = ''
            for tipo in tipos:
                tipo_field = tipo['Name'] + ', ' + tipo_field

            log_queryset = VentaLog.objects.filter(UserID=user_id).order_by('-Date').first()
            log_serializer = VentaLogUserSerializer(log_queryset)
            ultima_actividad = log_serializer.data['VentaLogType']

            cotizacion_data = Cotizacion.objects.all()
            cotizacion_queryset = cotizacion_data.filter(CotizacionStateID__Name=constants.COTIZATION_STATE[0])
            cotizationAction = self.get_data(ListCotizacionActionSerializer, cotizacion_queryset)

            # reserva_data = Reserva.objects.all()
            # reserva_pending_data = reserva_data.exclude(
            #     ReservaStateID__Name='Oferta')
            # reserva_queryset = reserva_data.filter(
            #     ReservaStateID__Name__in=[constants.RESERVA_STATE[0], constants.RESERVA_STATE[1]])
            # reservaAction = self.get_data(ListReservaActionSerializer, reserva_queryset)

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

            pendientes = dict(Cotizacion=cotizationAction,
                              # Reserva=reservaAction,
                              Ofertas=oferta_serializer.data,
                              Promesa=promesa_serializer.data)
            pendientes = ""
            total_uf_mes = promesa_data.count()
            total_uf_ano = promesa_data.count()
            proyectos_asignados = ""

            user_summary = UserSummary.objects.filter(
                UserId=user_id
            ).first()

            if user_summary is None:
                user_summary = UserSummary(
                    Nombre=nombre,
                    UserId=user_id,
                    Tipo=tipo_field,
                    UltimaActividad=ultima_actividad,
                    Pendientes=pendientes,
                    TotalUFMes=total_uf_mes,
                    TotalUFAno=total_uf_ano,
                    ProyectosAsignados=proyectos_asignados
                )
                user_summary.save()
            else:
                user_summary.Nombre = nombre,
                user_summary.UserId = user_id,
                user_summary.Tipo = tipo_field,
                user_summary.UltimaActividad = ultima_actividad,
                user_summary.Pendientes = pendientes,
                user_summary.TotalUFMes = total_uf_mes,
                user_summary.TotalUFAno = total_uf_ano,
                user_summary.ProyectosAsignados = proyectos_asignados
                user_summary.save()

        return Response({
            "logs": "ok",
        })
