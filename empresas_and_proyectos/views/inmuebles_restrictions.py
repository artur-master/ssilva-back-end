from django.shortcuts import get_object_or_404
from django.db.models import Q
from empresas_and_proyectos.models.inmuebles import Inmueble
from empresas_and_proyectos.models.inmuebles_restrictions import (
    InmuebleInmuebleType,
    InmuebleInmueble)
from empresas_and_proyectos.serializers.inmuebles_restrictions import (
    InmuebleInmuebleTypeSerializer,
    InmuebleRestrictionSerializer,
    SearchInmuebleRestrictionSerializer,
    InmuebleInmuebleRestrictionSerializer)
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class InmuebleInmuebleTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = InmuebleInmuebleTypeSerializer
    queryset = InmuebleInmuebleType.objects.all()


class InmuebleInmuebleRestrictionViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = InmuebleRestrictionSerializer
    queryset = InmuebleInmueble.objects.all()
    lookup_field = 'InmuebleID'

    def list(self, request):
        inmueble_id = self.request.query_params.get('q', None)
        inmueble = Inmueble.objects.get(InmuebleID=inmueble_id)
        queryset = InmuebleInmueble.objects.filter(
            Q(InmuebleAID=inmueble) | Q(InmuebleBID=inmueble)
        )
        serializer = SearchInmuebleRestrictionSerializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request):
        data = request.data
        serializer = InmuebleInmuebleRestrictionSerializer(
            data=data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            return Response({"detail": "Restricciones creadas con éxito",
                             "inmueble_restriction": SearchInmuebleRestrictionSerializer(instance, many=True).data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)

    def partial_update(self, request, InmuebleID):
        inmueble = get_object_or_404(Inmueble, InmuebleID=InmuebleID)
        inmueble_restricts = InmuebleInmueble.objects.filter(
            Q(InmuebleAID=inmueble) | Q(InmuebleBID=inmueble)
        )

        serializer = InmuebleInmuebleRestrictionSerializer(
            inmueble_restricts,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            instance = serializer.save()
            return Response({"detail": "Restricciones modificadas con éxito",
                             "inmueble_restriction": SearchInmuebleRestrictionSerializer(instance, many=True).data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)
