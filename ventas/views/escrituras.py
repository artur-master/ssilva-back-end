from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, APIException

from common.permissions import (
    CheckAdminOrConsOrMoniProyectosPermission,
    CheckAdminOrVendedorOrMoniProyectosPermission,
    CheckAdminOrConsCliPermission,
    CheckAdminOrConsUsersPermission)
from common.services import download_pdf_views
from empresas_and_proyectos.models.proyectos import Proyecto
from users.models import User

from ventas.models.escrituras import Escritura, AprobacionCredito
from ventas.serializers.escrituras import (
    ListEscrituraSerializer, RetrieveEscrituraSerializer, UpdateEscrituraSerializer,
    UpdateAprobacionCreditoSerializer,
    ConfirmProyectoSerializer, UpdateProyectoSerializer)
from empresas_and_proyectos.serializers.proyectos import (
    ProyectoSerializer, 
    RetrieveProyectoSerializer)
from ventas.serializers.promesas import RetrievePromesaSerializer
import json

class EscrituraViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ListEscrituraSerializer
    queryset = Escritura.objects.all()
    lookup_field = 'EscrituraID'

    # def get_permissions(self):
    #     if self.action == 'retrieve' or self.action == 'list':
    #         permission_classes = [IsAuthenticated, ]
    #     if self.action == 'create':
    #         permission_classes = [IsAuthenticated, ]
    #     if self.action == 'partial_update':
    #         permission_classes = [IsAuthenticated, ]
    #     return [permission() for permission in permission_classes]

    def list(self, request):
        proyecto_id = self.request.query_params.get('q', None)
        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        queryset = Escritura.objects.filter(ProyectoID=proyecto)

        queryset = ListEscrituraSerializer.setup_eager_loading(queryset)
        serializer = ListEscrituraSerializer(queryset, context={'request': request}, many=True)

        return Response(serializer.data)

    def retrieve(self, request, EscrituraID):
        queryset = Escritura.objects.all()
        queryset = RetrieveEscrituraSerializer.setup_eager_loading(queryset)
        instance = get_object_or_404(queryset, EscrituraID=EscrituraID)

        serializer = RetrieveEscrituraSerializer(
            instance, context={'request': request})
        promesa = RetrievePromesaSerializer(
            instance.PromesaID, context={'request': request})

        return Response({
            "escritura": serializer.data,
            "promesa": promesa.data
            })
        
    def partial_update(self, request, EscrituraID):
        serializer = UpdateEscrituraSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )
        
        if serializer.is_valid():
            instance = serializer.save()
            # escritura = self.get_object()
            
            return Response({"escritura": RetrieveEscrituraSerializer(
                                            instance, context={'request': request}).data,
                             "promesa": RetrievePromesaSerializer(
                                            instance.PromesaID, context={'request': request}).data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)

    @action(detail=True, methods=['patch'])
    def notificar(self, request, EscrituraID):
        serializer = UpdateEscrituraSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )
        
        if serializer.is_valid():
            instance = serializer.save()
            # escritura = self.get_object()
            project = instance.ProyectoID
            if project.EscrituraProyectoState<2:
                project.EscrituraProyectoState = 2
                project.save()

            return Response({"escritura": RetrieveEscrituraSerializer(
                                            instance, context={'request': request}).data,
                             "promesa": RetrievePromesaSerializer(
                                            instance.PromesaID, context={'request': request}).data
                            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)

        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)

    @action(detail=True, methods=['patch'])
    def aprova_credit(self, request, EscrituraID):
        data = request.data

        many = isinstance(data, list)
        serializer = UpdateEscrituraSerializer(
            self.get_object(), data=data, partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            instance = serializer.save()
            # escritura = self.get_object()
            
            creditos = AprobacionCredito.objects.filter(EscrituraID=instance)
            if creditos.exists():
                creditos.delete()
            
            creditosNumber = int(data.get("CreditosNumber"))
            credito_list = list()
            for i in range(creditosNumber):
                credito = AprobacionCredito(                    
                    FormalCredit = data.get("AprobacionCreditos.{}.FormalCredit".format(i)),
                    BankName = data.get("AprobacionCreditos.{}.BankName".format(i)),
                    ExecutiveEmail = data.get("AprobacionCreditos.{}.ExecutiveEmail".format(i)),
                    ExecutiveName = data.get("AprobacionCreditos.{}.ExecutiveName".format(i)),
                    ClientPersonalHealthStatement = 
                        data.get("AprobacionCreditos.{}.ClientPersonalHealthStatement".format(i), None),
                    AcFinancialInstitution = 
                        data.get("AprobacionCreditos.{}.AcFinancialInstitution".format(i), None),                    
                    EscrituraID = instance)
                credito_list.append(credito)
            if credito_list:
                AprobacionCredito.objects.bulk_create(credito_list)

            return Response({"escritura": RetrieveEscrituraSerializer(
                                            instance, context={'request': request}).data,
                             "promesa": RetrievePromesaSerializer(
                                            instance.PromesaID, context={'request': request}).data
                            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)

    @action(detail=True, methods=['patch'])
    def check_credit(self, request, EscrituraID):
        data = request.data

        # many = isinstance(data, list)
        serializer = UpdateEscrituraSerializer(
            self.get_object(), data=data, partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            # escritura = self.get_object()
            
            creditosNumber = int(data.get("CreditosNumber"))
            for i in range(creditosNumber):
                credito = AprobacionCredito.objects.get(
                    AprobacionCreditoID=data.get("AprobacionCreditos.{}.AprobacionCreditoID".format(i)))
                print(data)
                credito.AprobacionCreditoState=(data.get("AprobacionCreditos.{}.AprobacionCreditoState".format(i))=='1')
                if "AprobacionCreditos.{}.AcObservations".format(i) in data:
                    credito.AcObservations= json.loads(data.get("AprobacionCreditos.{}.AcObservations".format(i)))

                credito.save()
                
            instance = serializer.save()
            return Response({"escritura": RetrieveEscrituraSerializer(
                                            instance, context={'request': request}).data,
                             "promesa": RetrievePromesaSerializer(
                                            instance.PromesaID, context={'request': request}).data
                            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class EscrituraProyectoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProyectoSerializer
    queryset = Proyecto.objects.all()
    lookup_field = 'ProyectoID'

    def partial_update(self, request, ProyectoID):
        serializer = UpdateProyectoSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )
        if serializer.is_valid():
            instance = serializer.save()
            retrieve_serializer = RetrieveProyectoSerializer(instance, context={'request': request})
            return Response({"proyecto": retrieve_serializer.data,
                             "detail": "Proyecto confirmado con éxito."},
                            status=status.HTTP_200_OK)
        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)

        
    @action(detail=True, methods=['patch'])
    def confirm_escritura(self, request, ProyectoID):
        proyecto = Proyecto.objects.get(ProyectoID=ProyectoID)
        # queryset = Escritura.objects.filter(ProyectoID=proyecto)
        
        serializer = ConfirmProyectoSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            retrieve_serializer = RetrieveProyectoSerializer(instance, context={'request': request})
            return Response({"proyecto": retrieve_serializer.data,
                            "detail": "Proyecto actualizado con éxito."},
                            status=status.HTTP_200_OK)
        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)