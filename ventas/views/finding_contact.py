from ventas.models.finding_contact import (
    FindingType,
    ContactMethodType)
from ventas.serializers.finding_contact import (
    FindingTypeSerializer,
    ContactMethodTypeSerializer)
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class FindingTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = FindingTypeSerializer
    queryset = FindingType.objects.all()
    lookup_field = 'FindingTypeID'


class ContactMethodTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactMethodTypeSerializer
    queryset = ContactMethodType.objects.all()


