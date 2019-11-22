from empresas_and_proyectos.models.constructoras import Constructora
from users.serializers.constructoras import ConstructoraTypeSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class ConstructoraViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ConstructoraTypeSerializer

    def get_queryset(self):
        queryset = Constructora.objects.filter(State=True)
        return queryset
