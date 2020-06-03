from django.http import HttpResponse
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
import requests
import json

from common import constants
from common.permissions import (
    CheckAdminOrConsOrMoniProyectosPermission,
    CheckAdminOrVendedorOrMoniProyectosPermission,
    CheckAdminOrConsCliPermission,
    CheckAdminOrConsUsersPermission)
from common.services import download_pdf_views
from common.models import ContactInfoType
from empresas_and_proyectos.models.proyectos import Proyecto
from users.models import User
from ventas.models.clientes import Cliente, ClienteContactInfo
from ventas.models.cotizaciones import (
    Cotizacion,
    CotizacionType,
    CotizacionState)
from ventas.models.finding_contact import ContactMethodType
from ventas.models.payment_forms import PayType

from ventas.serializers.cotizaciones import (
    CotizacionTypeSerializer,
    CotizacionSerializer,
    DownloadCotizacionSerializer,
    CreateCotizacionSerializer)
from ventas.snippets.clientes_serializers import save_cliente
from empresas_and_proyectos.models.proyectos import ProyectoContactInfo

class CotizacionTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CotizacionTypeSerializer
    queryset = CotizacionType.objects.all()


class CotizacionProyectoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        CheckAdminOrConsOrMoniProyectosPermission)
    serializer_class = CotizacionSerializer
    queryset = Cotizacion.objects.all()
    lookup_field = 'CotizacionID'

    def list(self, request):
        proyecto_id = self.request.query_params.get('q', None)
        proyecto = Proyecto.objects.get(ProyectoID=proyecto_id)
        queryset = Cotizacion.objects.filter(ProyectoID=proyecto)
        queryset = CotizacionSerializer.setup_eager_loading(queryset)
        serializer = CotizacionSerializer(queryset, many=True)

        return Response(serializer.data)


class DownloadCotizacionProyectoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DownloadCotizacionSerializer
    queryset = Cotizacion.objects.all()
    lookup_field = 'CotizacionID'

    def create(self, request):
        data = request.data
        serializer = DownloadCotizacionSerializer(data=data)

        if serializer.is_valid():
            cotizacion_id = serializer.validated_data.get("CotizacionID")
            letter_size = serializer.validated_data.get("LetterSize")
            response = HttpResponse(content_type='application/pdf')
            pdf = download_pdf_views(cotizacion_id, letter_size, response)
            response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % (
                pdf['name'])
            return response
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class CotizacionViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CotizacionSerializer
    queryset = Cotizacion.objects.all()
    lookup_field = 'CotizacionID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated,
                                  CheckAdminOrConsOrMoniProyectosPermission, ]
        else:
            permission_classes = [
                IsAuthenticated,
                CheckAdminOrVendedorOrMoniProyectosPermission,
            ]
        return [permission() for permission in permission_classes]

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = CreateCotizacionSerializer(
            data=data, many=many, context={'request': request})

        if serializer.is_valid():
            instance = serializer.save()
            return Response({"detail": "Cotización creada con éxito",
                             "cotizacion": CotizacionSerializer(instance).data},
                            status=status.HTTP_201_CREATED)

        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)


class CotizacionesClienteViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminOrConsCliPermission)
    serializer_class = CotizacionSerializer
    queryset = Cotizacion.objects.all()
    lookup_field = 'CotizacionID'

    def list(self, request):
        cliente_id = self.request.query_params.get('q', None)
        cliente = Cliente.objects.get(UserID=cliente_id)
        queryset = Cotizacion.objects.filter(ClienteID=cliente)
        queryset = CotizacionSerializer.setup_eager_loading(queryset)
        serializer = CotizacionSerializer(queryset, many=True)

        return Response(serializer.data)


class CotizacionesCotizadorViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckAdminOrConsUsersPermission)
    serializer_class = CotizacionSerializer
    queryset = Cotizacion.objects.all()
    lookup_field = 'CotizacionID'

    def list(self, request):
        cotizador_id = self.request.query_params.get('q', None)
        cotizador = User.objects.get(UserID=cotizador_id)
        queryset = Cotizacion.objects.filter(CotizadorID=cotizador)
        queryset = CotizacionSerializer.setup_eager_loading(queryset)
        serializer = CotizacionSerializer(queryset, many=True)

        return Response(serializer.data)


class PreCotizacionViewSet(viewsets.ModelViewSet):
    serializer_class = CotizacionSerializer
    queryset = Cotizacion.objects.all()
    lookup_field = 'CotizacionID'
    apiToken = settings.PIPEDRIVE_API_TOKEN

    def create(self, request):
        data = request.data
        
        current_pipeline_id = data['current']['stage_id']
        previous_pipeline_id = data['previous']['stage_id']

        if current_pipeline_id != 2 or previous_pipeline_id != 1:
            return Response({"detail": "cann't create cotizacion"},
                            status=status.HTTP_409_CONFLICT)

        deal_id = data['current']['id']
        dealInfo = self.get_deal(deal_id)

        clientRut = dealInfo['cRut']
        clientName = dealInfo['cName']
        clientEmail = dealInfo['cEmail']
        clientPhone = dealInfo['cPhone']
        clientMedio = dealInfo['cMedio']

        dealTile = dealInfo['Title']

        userName = dealInfo['userName']
        userEmail = dealInfo['userEmail']

        projectEmail = dealInfo['projectEmail']
        projectName = dealInfo['projectName']

        try:
            current_user = User.objects.get(Email=userEmail)
        except User.DoesNotExist:
            raise ValidationError('You are unregistered user.')
        
        try:
            info=ProyectoContactInfo.objects.get(
                Value=projectEmail,
                ProyectoID__Name=projectName,
                ProyectoID__BorradorPromesaState__Name=constants.BORRADOR_PROMESA_STATE[1])
            project = info.ProyectoID

            try:
                client = Cliente.objects.get(user_ptr__Rut=clientRut)
            except Cliente.DoesNotExist:
                client = Cliente(Name=clientName, Rut=clientRut, Email=clientEmail, Creator=current_user, LastModifier=current_user)
                client.save()

                contactInfoEmailType = ContactInfoType.objects.get(Name="Email")
                contactInfo = ClienteContactInfo(Value=clientEmail, ContactInfoTypeID=contactInfoEmailType, UserID=client)
                contactInfo.save()
                contactInfoPhoneType = ContactInfoType.objects.get(Name="Phone")
                contactInfo = ClienteContactInfo(Value=clientPhone, ContactInfoTypeID=contactInfoPhoneType, UserID=client)
                contactInfo.save()
            
            try:
                cotizacion_state = CotizacionState.objects.get(
                    Name=constants.COTIZATION_STATE[0]) #Vigente
                cotizacion_type = CotizacionType.objects.get(
                    Name=constants.COTIZATION_TYPE[0])  #Presencial/No Presencial
                contact_method_type = ContactMethodType.objects.get(
                    Name=constants.CONTACT_METHOD_TYPE[1]) #Mail
                paytype = PayType.objects.get(
                    Name=constants.PAY_TYPE[0]) #Contado/Credito

                instance = Cotizacion.objects.create(
                    ProyectoID=project,
                    ClienteID=client,
                    CotizadorID=current_user,
                    Vendedor = current_user,
                    CotizacionStateID = cotizacion_state,
                    CotizacionTypeID = cotizacion_type,
                    ContactMethodTypeID = contact_method_type,
                    PayType = paytype,
                    Folio=dealTile)

                instance.save()

                return Response({"detail": "Cotización creada con éxito",
                                "cotizacion": CotizacionSerializer(instance).data},
                                status=status.HTTP_201_CREATED)
            except:
                return Response({"detail": "error"},
                        status=status.HTTP_409_CONFLICT)
            
        except ProyectoContactInfo.DoesNotExist:
            raise ValidationError('Proyecto does not exist')

    def get_deal(self, id):
        url = "https://api.pipedrive.com/v1/deals/{}?api_token={}".format(id, self.apiToken)
        data = requests.get(url)
        data = json.loads(data.text)

        dealTitle = data['data']['title']

        userName = data['data']['user_id']['name']
        userEmail = data['data']['user_id']['email']

        cId = data['data']['person_id']['value']
        cRut = self.get_clientRut(cId)
        
        cName = data['data']['person_name']
        cEmail = data['data']['person_id']['email'][0]['value']
        cPhone = data['data']['person_id']['phone'][0]['value']
        
        medioDeLlegada = data['data']['afa87cd73eb2ec817381b015fb13983819962b93']
        clientMedio = self.get_customField(12507, int(medioDeLlegada))

        projectNameId = data['data']['32d6fb2f290514fc3a79b271c382783b00649c97']
        projectName = self.get_customField(12500, int(projectNameId))

        projectEmail = data['data']['user_id']['email']
        return {
            'Title':dealTitle,
            'userName': userName,
            'userEmail': userEmail,
            'cRut':cRut,
            'cName':cName,
            'cEmail':cEmail,
            'cPhone':cPhone,
            'cMedio':clientMedio,
            'projectName':projectName,
            'projectEmail': projectEmail
        }
    
    def get_clientRut(self, cId):
        url = "https://api.pipedrive.com/v1/persons/{}?api_token={}".format(cId, self.apiToken)
        data = requests.get(url)
        data = json.loads(data.text)

        return data['data']['c462f1632cc062acf9b58f530d3c1b6b3aa35aa4']

    def get_customField(self, id, select):
        url = "https://api.pipedrive.com/v1/dealFields/{}?api_token={}".format(id, self.apiToken)
        data = requests.get(url)
        data = json.loads(data.text)

        for key in data['data']['options']:
            if key['id'] == select:
                return key['label']
        
        return None