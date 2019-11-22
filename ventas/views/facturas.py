from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import CheckProyectoFinazaPermission
from empresas_and_proyectos.models.proyectos import Proyecto
from ventas.models.facturas import ComisionInmobiliaria, FacturaInmueble, Factura
from ventas.serializers.facturas import (
    CreateComisionesSerializer, UpdateComisionesSerializer, ComisionesSerializer,
    FacturaInmuebleSerializer, RetrieveFacturaSerializer, ListFacturaSerializer, download_factura,
    download_nota_credito, RegisterSendFacturaSerializer, RegisterDatePagoFacturaSerializer)


class ComisionInmobiliariaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateComisionesSerializer
    queryset = ComisionInmobiliaria.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated, CheckProyectoFinazaPermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        proyecto_id = self.request.query_params.get('q', None)
        try:
            proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
            queryset = ComisionInmobiliaria.objects.get(ProyectoID=proyecto)
        except Proyecto.DoesNotExist:
            return Response("Project %s does not exist" % proyecto_id, status=400)
        except ComisionInmobiliaria.DoesNotExist:
            return Response(dict(), status=204)
        serializer = ComisionesSerializer(queryset)

        return Response(serializer.data)

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = CreateComisionesSerializer(
            data=data, many=many, context={'request': request})

        if serializer.is_valid():
            comission = serializer.create(data)
            return Response({"detail": "Comisiones agregadas con éxito",
                             "comisiones": dict(ProyectoID=comission.ProyectoID.ProyectoID,
                                                PromesaFirmada=comission.PromesaFirmada,
                                                EscrituraFirmada=comission.EscrituraFirmada,
                                                CierreGestion=comission.CierreGestion,
                                                State=comission.State,
                                                NoExisted=comission.NoExisted)},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class UpdateComisionesAPIView(APIView):

    def patch(self, request, proyecto_id):
        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        comisiones = ComisionInmobiliaria.objects.get(ProyectoID=proyecto)
        serializer = UpdateComisionesSerializer(comisiones, data=request.data, partial=True)
        if serializer.is_valid():
            comission = serializer.save()
            return Response({"detail": "Comisiones modificadas con éxito",
                             "comisiones": dict(ProyectoID=comission.ProyectoID.ProyectoID,
                                                PromesaFirmada=comission.PromesaFirmada,
                                                EscrituraFirmada=comission.EscrituraFirmada,
                                                CierreGestion=comission.CierreGestion,
                                                State=comission.State,
                                                NoExisted=comission.NoExisted
                                                )},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class FacturaInmuebleViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = FacturaInmuebleSerializer
    queryset = FacturaInmueble.objects.all()

    def list(self, request):
        proyecto_id = self.request.query_params.get('q', None)
        state = self.request.query_params.get('s', None)
        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        queryset = FacturaInmueble.objects.filter(ProyectoID=proyecto, State=state)
        if not queryset:
            message = "No hay inmuebles en estado {state}".format(state=state)
            return Response({"detail": message},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = FacturaInmuebleSerializer(queryset, many=True)
            return Response(serializer.data)


class FacturaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RetrieveFacturaSerializer
    queryset = Factura.objects.all()
    lookup_field = 'FacturaID'

    def list(self, request):
        proyecto_id = self.request.query_params.get('q', None)
        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        queryset = Factura.objects.filter(ProyectoID=proyecto)
        if not queryset:
            return Response({"detail": "No hay facturas"},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ListFacturaSerializer(queryset, many=True)
            return Response(serializer.data)

    def retrieve(self, request, FacturaID):
        queryset = Factura.objects.all()
        instance = get_object_or_404(queryset, FacturaID=FacturaID)
        serializer = RetrieveFacturaSerializer(
            instance, context={'request': request})

        return Response(serializer.data)


class DownloadFacturaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = ComisionesSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Factura.objects.all()
    lookup_field = 'FacturaID'

    def partial_update(self, request, FacturaID):
        response = HttpResponse(content_type='application/pdf')
        pdf = download_factura(self.get_object(), response)
        response['Content-Disposition'] = 'inline; filename="%s.pdf"' % (pdf)
        return response


class DownloadNotaCreditoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = ComisionesSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Factura.objects.all()
    lookup_field = 'FacturaID'

    def partial_update(self, request, FacturaID):
        response = HttpResponse(content_type='application/pdf')
        pdf = download_nota_credito(self.get_object(), response)
        response['Content-Disposition'] = 'inline; filename="%s.pdf"' % (pdf)
        return response


class RegisterSendFacturaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = RegisterSendFacturaSerializer
    queryset = Factura.objects.all()
    lookup_field = 'FacturaID'

    def partial_update(self, request, FacturaID):
        serializer = RegisterSendFacturaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"factura": serializer.data,
                             "detail": "Registro envio de factura con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class RegisterDatePagoFacturaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = RegisterDatePagoFacturaSerializer
    queryset = Factura.objects.all()
    lookup_field = 'FacturaID'

    def partial_update(self, request, FacturaID):
        serializer = RegisterDatePagoFacturaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"factura": serializer.data,
                             "detail": "Registro pago de factura con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)
