from empresas_and_proyectos.models.inmobiliarias import Inmobiliaria
from users.serializers.inmobiliarias import InmobiliariaTypeSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class InmobiliariaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = InmobiliariaTypeSerializer

    def get_queryset(self):
        queryset = Inmobiliaria.objects.filter(State=True)
        return queryset
