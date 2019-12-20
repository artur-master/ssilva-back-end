from rest_framework.permissions import IsAuthenticated

from common.snippets.checks.generate_new_bank_check import generate_new_check
from common.snippets.checks.generate_old_bank_check import generate_old_check
from users.models import Nationality
from common import constants
from ventas.models.cotizaciones import CotizacionType
from ventas.models.finding_contact import FindingType, ContactMethodType
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from ventas.models.payment_forms import PayType
from ventas.serializers.paytypes import PayTypeSerializer
from ventas.snippets.utils import return_required_documents


class UtilsClientesViewSet(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        nationalities = Nationality.objects.all().order_by('name').values_list('name', flat=True)

        return Response({'Genres': constants.GENRES,
                         'CivilStatus': constants.CIVIL_STATUS,
                         'ContractMarriageTypes': constants.CONTRACT_MARRIAGE_TYPES,
                         'Nationality_type': constants.NATIONALITIES_TYPES,
                         'Nationalities': nationalities,
                         'Antiquities': constants.ANTIQUITIES,
                         'Salaries': constants.SALARY_RANK,
                         'Ages': constants.AGE_RANK},
                        status=status.HTTP_200_OK)


class GenerateCheckViewSet(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        body = request.data

        if body.get('NewFormat'):
            response = generate_new_check(
                body.get('City'), body.get('Date'), body.get('Number'), body.get('HasYear'),
                body.get('Beneficiary'), body.get('Nominative'),
                body.get('Crossed'), body.get('ToTheCarrier'), body.get('AccountNumber'))
        else:
            response = generate_old_check(
                body.get('Date'), body.get('Number'), body.get('HasYear'),
                body.get('Beneficiary'), body.get('Nominative'),
                body.get('Crossed'), body.get('ToTheCarrier'), body.get('AccountNumber'))

        return response


class UtilsCotizacionViewSet(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        finding_types = FindingType.objects.all().values('Name', 'FindingTypeID')
        contact_method_types = ContactMethodType.objects.all().values('Name', 'ContactMethodTypeID')
        cotizacion_types = CotizacionType.objects.all().values('Name', 'CotizacionTypeID')

        return Response({'FindingTypes': finding_types,
                         'ContactMethodTypes': contact_method_types,
                         'CotizacionTypes': cotizacion_types,
                         },
                        status=status.HTTP_200_OK)


class RequiredDocumentsViewSet(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        documents = return_required_documents()

        return Response({'Documents': documents},
                        status=status.HTTP_200_OK)


class UtilsPaymentViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PayTypeSerializer
    queryset = PayType.objects.all()
    http_method_names = ['get']
