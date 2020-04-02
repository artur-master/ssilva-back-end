from rest_framework.views import APIView
from rest_framework.decorators import action
from common.permissions import (
    CheckAdminOrConsParamPermission,
    CheckAdminParamPermission)
from empresas_and_proyectos.models.inmuebles import (
    InmuebleType,
    Tipologia,
    Inmueble,
    Orientation, InmuebleState)
from empresas_and_proyectos.serializers.inmuebles import (
    InmuebleTypeSerializer,
    TipologiaSerializer,
    InmuebleSerializer,
    ListOrientationSerializer, InmuebleStateSerializer)
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_bulk_update.helper import bulk_update


class InmuebleTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = InmuebleTypeSerializer
    queryset = InmuebleType.objects.all()
    lookup_field = 'InmuebleTypeID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            # permission_classes = [IsAuthenticated,
            #                       CheckAdminOrConsParamPermission, ]
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, CheckAdminParamPermission, ]
        return [permission() for permission in permission_classes]


class TipologiaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = TipologiaSerializer
    queryset = Tipologia.objects.all()
    lookup_field = 'TipologiaID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            # permission_classes = [IsAuthenticated,
            #                       CheckAdminOrConsParamPermission, ]
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, CheckAdminParamPermission, ]
        return [permission() for permission in permission_classes]


class OrientationViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ListOrientationSerializer
    queryset = Orientation.objects.all()
    lookup_field = 'OrientationID'


class InmuebleStateViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = InmuebleStateSerializer
    queryset = InmuebleState.objects.all()
    lookup_field = 'InmuebleStateID'


class InmuebleViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = InmuebleSerializer
    queryset = Inmueble.objects.all()
    lookup_field = 'InmuebleID'
    
    def create(self, request):
        datas = request.FILES
        for data in datas:
            default={'Up_Print': datas[data]}
            try:
                up_file = Inmueble.objects.get(InmuebleID=data)
                if up_file.Up_Print:
                    up_file.Up_Print.delete()
                for key, value in default.items():
                    setattr(up_file, key, value)
                up_file.save()
            except:
                print('error')
        Inmueble_ID = list(datas)[0]
        etapaID = Inmueble.objects.get(InmuebleID=Inmueble_ID).EtapaID
        queryset = Inmueble.objects.filter(EtapaID=etapaID)
        serializer = InmuebleSerializer(queryset, many=True)
        return Response({"entities":serializer.data, "message": "success uploaded"}, status=status.HTTP_200_OK)


class UpdateInmueblesViewSet(APIView):

    def update_changed_fields(self, item, changed, orientations):
        for k in changed.get('Changes', {}):
            if k.lower() == 'orientation':
                item.OrientationID.clear()
                for name in changed.get('OrientationNames'):
                    ori = orientations.get(Name=name.get('OrientationID'))
                    item.OrientationID.add(ori)
            elif k.lower() == 'number':
                item.Number = changed.get('Number')
            elif k.lower() == 'floor':
                item.Floor = changed.get('Floor')
            elif k.lower() == 'bedrooms':
                item.BedroomsQuantity = changed.get('BedroomsQuantity')
            elif k.lower() == 'bathrooms':
                item.BathroomQuantity = changed.get('BathroomQuantity')
            elif k.lower() == 'util':
                item.UtilSquareMeters = changed.get('UtilSquareMeters')
            elif k.lower() == 'total':
                item.TotalSquareMeters = changed.get('TotalSquareMeters')
            elif k.lower() == 'terrace':
                item.TerraceSquareMeters = changed.get('TerraceSquareMeters')
            elif k.lower() == 'lodge':
                item.LodgeSquareMeters = changed.get('LodgeSquareMeters')
            elif k.lower() == 'price':
                item.Price = changed.get('Price')
            elif k.lower() == 'discount':
                item.MaximunDiscount = changed.get('MaximunDiscount')
            elif k.lower() == 'tipologia':
                item.TipologiaID = Tipologia.objects.get(
                    TipologiaID=changed.get('TipologiaID'))
            elif k.lower() == 'type':
                item.InmuebleTypeID = InmuebleType.objects.get(
                    InmuebleTypeID=changed.get('InmuebleTypeID'))
                if changed.get('InmuebleTypeName').strip().lower() in 'bodega':
                    item.OrientationID.clear()
                    item.BedroomsQuantity = 0
                    item.BathroomQuantity = 0
                    item.TipologiaID = None
                elif changed.get('InmuebleTypeName').strip().lower() == 'estacionamiento':
                    item.OrientationID.clear()
                    item.BedroomsQuantity = 0
                    item.BathroomQuantity = 0
                    item.TipologiaID = None
                elif changed.get('InmuebleTypeName').strip().lower() == 'casa':
                    item.OrientationID.clear()
                    item.TipologiaID = None
                    item.Floor = 0
                elif changed.get('InmuebleTypeName').lower().find('comercial'):
                    item.BedroomsQuantity = 0
                    item.TipologiaID = None

    def patch(self, request, *args, **kwargs):
        data = request.data
        inmueble_uuids = [inmueble.get('InmuebleID', '') for inmueble in data]
        inmuebles = Inmueble.objects.filter(InmuebleID__in=inmueble_uuids)
        orientations = Orientation.objects.all()
        list_to_update = list()
        for changed in data:
            try:
                inmueble = inmuebles.get(InmuebleID=changed['InmuebleID'])
                self.update_changed_fields(inmueble, changed, orientations)
                list_to_update.append(inmueble)
            except Exception:
                pass
        bulk_update(list_to_update)
        return Response({"message": "success patched"})

