from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from common.permissions import CheckAdminMoniProyectosPermission
from empresas_and_proyectos.models.etapas import EtapaState, Etapa
from empresas_and_proyectos.models.proyectos import Proyecto
from empresas_and_proyectos.serializers.etapas import (
    EtapaStateSerializer,
    EtapaSerializer,
    ListEtapaSerializer,
    CreateMassiveEtapaInmueblesSerializer,
    CreateEtapaSerializer,
    UpdateEtapaSerializer,
    CreateEtapaSingleSerializer)
from rest_framework import viewsets, status, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from empresas_and_proyectos.serializers.inmuebles import InmuebleSerializer


class EtapaStateViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = EtapaStateSerializer
    queryset = EtapaState.objects.all()
    lookup_field = 'EtapaStateID'


class EtapaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = EtapaSerializer
    queryset = Etapa.objects.all()
    lookup_field = 'EtapaID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated,
                                  CheckAdminMoniProyectosPermission, ]
        return [permission() for permission in permission_classes]

    def list(self, request):
        proyecto_id = self.request.query_params.get('q', None)
        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        queryset = Etapa.objects.filter(ProyectoID=proyecto)
        queryset = ListEtapaSerializer.setup_eager_loading(queryset)
        serializer = ListEtapaSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, EtapaID):
        queryset = Etapa.objects.all()
        queryset = ListEtapaSerializer.setup_eager_loading(queryset)
        instance = get_object_or_404(queryset, EtapaID=EtapaID)

        serializer = ListEtapaSerializer(instance)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = EtapaSerializer(
            data=data, context={'request': request}, many=many)
        if serializer.is_valid():
            instance = serializer.save()
            etapa_serializer = ListEtapaSerializer(instance, many=many)
            return Response({"detail": "Inmuebles modificados con éxito",
                             "etapa": etapa_serializer.data},
                            status=status.HTTP_200_OK)
        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)


class CreateMassiveEtapaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminMoniProyectosPermission)
    serializer_class = CreateMassiveEtapaInmueblesSerializer
    queryset = Etapa.objects.all()
    lookup_field = 'EtapaID'

    def partial_update(self, request, EtapaID):
        serializer = CreateMassiveEtapaInmueblesSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request})

        if serializer.is_valid():
            inmuebles = serializer.upload(self.get_object(), serializer.initial_data)
            return Response({"detail": "Inmuebles agregados con éxito",
                             "inmuebles": inmuebles},
                            status=status.HTTP_200_OK)
        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)

    @action(detail=True, methods=['post'])
    def save(self, request, EtapaID):
        serializer = CreateMassiveEtapaInmueblesSerializer(self.get_object(),
                                                           data=request.data,
                                                           context={'request': request})

        serializer.save_db(self.get_object(), serializer.initial_data)
        return Response({"detail": "Inmuebles agregados con éxito",
                         "inmuebles": serializer.initial_data['data']},
                        status=status.HTTP_200_OK)


class CreateEtapaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminMoniProyectosPermission)
    serializer_class = CreateEtapaSerializer
    queryset = Etapa.objects.all()
    lookup_field = 'EtapaID'

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = CreateEtapaSerializer(
            data=data, many=many, context={'request': request})

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"detail": "Etapa agregados con éxito",
                             "etapas": ListEtapaSerializer(instance, many=many).data},
                            status=status.HTTP_201_CREATED)
        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)

    def partial_update(self, request, EtapaID):
        serializer = UpdateEtapaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request})

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"detail": "Etapa modificada con éxito",
                             "etapas": ListEtapaSerializer(instance).data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class CreateEtapaSingleViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminMoniProyectosPermission)
    serializer_class = CreateEtapaSingleSerializer
    queryset = Etapa.objects.all()
    lookup_field = 'EtapaID'

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = CreateEtapaSingleSerializer(
            data=data, many=many, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Etapa creada con éxito",
                             "etapa": serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)
