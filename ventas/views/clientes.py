from common.permissions import (
    CheckAdminOrConsCliPermission,
    CheckAdminCliPermission)
from ventas.models.clientes import Cliente
from ventas.serializers.clientes import (
    ClienteSerializer,
    ListClienteSerializer,
    CreateClienteSerializer,
    UpdateClienteSerializer)
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class ClienteViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()
    lookup_field = 'UserID'
       
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [
                IsAuthenticated, CheckAdminOrConsCliPermission, ]
        else:
            permission_classes = [IsAuthenticated, CheckAdminCliPermission, ]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = Cliente.objects.all()
        serializer = ListClienteSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = CreateClienteSerializer(
            data=data, many=many, context={
                'request': request})

        if serializer.is_valid():
            instance = serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response({"cliente": ListClienteSerializer(instance, many=many).data,
                             "detail": "Cliente creado con éxito"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)

    def partial_update(self, request, UserID):
        serializer = UpdateClienteSerializer(
            self.get_object(), data=request.data, partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"cliente": ListClienteSerializer(instance).data,
                             "detail": "Cliente modificado con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)

    def destroy(self, request, UserID):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"cliente": UserID, "detail": "Cliente eliminada"},
                             status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)