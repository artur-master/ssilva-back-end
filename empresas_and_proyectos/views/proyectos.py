from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser

from common import constants
from empresas_and_proyectos.models.inmuebles_restrictions import InmuebleInmueble
from empresas_and_proyectos.models.project_documents import ProjectDocument
from empresas_and_proyectos.models.proyectos import (
    Proyecto,
    UserProyectoType)
from empresas_and_proyectos.serializers.proyectos import (
    ProyectoSerializer,
    RetrieveProyectoSerializer,
    CreateProyectoSerializer,
    UpdateProyectoSerializer,
    UserProyectoTypeSerializer,
    ApproveCreateProyectoGerenciaSerializer,
    ApproveCreateProyectoLegalSerializer,
    SendProyectoGerenciaSerializer,
    SendProyectoLegalSerializer,
    AddBorradorPromesaSerializer, UpdateProyectoMarketingSerializer, UpdateProyectoLegalSerializer,
    ReviewProjectDocumentSerializer, ProyectoRestrictionSerializer)
from common.notifications import (
    eliminar_notificacion_proyecto_aprobado,
    eliminar_notificacion_proyecto_rechazado)
from common.permissions import (
    list_proyectos_by_permission,
    CheckAdminMoniProyectosPermission,
    CheckMonitorProyectosPermission,
    CheckApproveInmueblesPermission, CheckProyectoMarketingPermission, CheckProyectoLegalPermission)
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ProyectoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProyectoSerializer
    queryset = Proyecto.objects.all()
    lookup_field = 'ProyectoID'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated, CheckAdminMoniProyectosPermission]
        elif self.action == 'partial_update':
            permission_classes = [IsAuthenticated, CheckAdminMoniProyectosPermission]
        elif self.action == 'marketing':
            permission_classes = [IsAuthenticated, CheckProyectoMarketingPermission]
        elif self.action == 'legal':
            permission_classes = [IsAuthenticated, CheckProyectoLegalPermission]
        elif self.action == 'review_document':
            permission_classes = [IsAuthenticated, CheckProyectoLegalPermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = list_proyectos_by_permission(request.user)
        serializer = RetrieveProyectoSerializer(
            queryset, many=True, context={
                'request': request})
        return Response(serializer.data)

    def retrieve(self, request, ProyectoID):
        queryset = list_proyectos_by_permission(request.user)
        queryset = RetrieveProyectoSerializer.setup_eager_loading(queryset)
        instance = get_object_or_404(queryset, ProyectoID=ProyectoID)
        current_user = request.user

        eliminar_notificacion_proyecto_aprobado(instance, current_user)
        eliminar_notificacion_proyecto_rechazado(instance, current_user)

        serializer = RetrieveProyectoSerializer(
            instance, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = CreateProyectoSerializer(
            data=data, many=many, context={'request': request})
        if serializer.is_valid():
            instance = serializer.create(data)
            retrieve_serializer = RetrieveProyectoSerializer(instance, context={'request': request})
            return Response({"proyecto": retrieve_serializer.data,
                             "detail": "Proyecto creado con éxito"},
                            status=status.HTTP_201_CREATED)
        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)

    def partial_update(self, request, ProyectoID):
        serializer = UpdateProyectoSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            instance = serializer.save()
            retrieve_serializer = RetrieveProyectoSerializer(instance, context={'request': request})
            return Response({"proyecto": retrieve_serializer.data,
                             "detail": "Proyecto modificado con éxito"},
                            status=status.HTTP_200_OK)
        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)

    def upload(self, serializer, request, doc_type, doc_type_message):
        if serializer.is_valid():
            obj = serializer.upload(self.get_object())
            base_url = "http://" + get_current_site(request).domain
            documents = dict()
            for mtype in doc_type:
                try:
                    document = obj.Documents.get(DocumentType=mtype)
                    documents[mtype] = {
                        "url": base_url + document.Document.url,
                        "state": document.State,
                        "document_type": document.DocumentType,
                        "no_existed": document.NoExisted
                    }
                except ProjectDocument.DoesNotExist:
                    documents[mtype] = None
                except ValueError:
                    documents[mtype] = {
                        "url": None,
                        "state": document.State,
                        "document_type": document.DocumentType,
                        "no_existed": document.NoExisted
                    }
            return Response({"documentos": documents,
                             "detail": "Documentos de %s actualizados" % doc_type_message},
                            status=status.HTTP_200_OK)
        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)

    @action(detail=True, methods=['put'])
    def marketing(self, request, ProyectoID):
        serializer = UpdateProyectoMarketingSerializer(data=request.data, context={'request': request})
        marketing_type = constants.MarketingDocumentTypes.values()
        return self.upload(serializer, request, marketing_type, 'marketing')

    @action(detail=True, methods=['put'])
    def legal(self, request, ProyectoID):
        serializer = UpdateProyectoLegalSerializer(data=request.data, context={'request': request})
        legal_type = constants.LegalDocumentTypes.values()
        return self.upload(serializer, request, legal_type, 'legal')

    @action(detail=True, methods=['patch'])
    def review_document(self, request, ProyectoID):
        serializer = ReviewProjectDocumentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.review(self.get_object(), serializer.initial_data)
            return Response(serializer.initial_data)
        return Response({"detail": serializer.errors},
                        status=status.HTTP_409_CONFLICT)

    @action(detail=True, methods=['get'])
    def restrictions(self, request, ProyectoID):
        try:
            proyecto_id = Proyecto.objects.get(ProyectoID=ProyectoID)
            restrictions = InmuebleInmueble.objects.all()
            restrictions = restrictions.select_related('InmuebleAID__EtapaID__ProyectoID', 'InmuebleInmuebleTypeID')
            restrictions = restrictions.filter(InmuebleAID__EtapaID__ProyectoID=proyecto_id)

            data = ProyectoRestrictionSerializer(restrictions).to_dict()
            # from django.db import connection
            # print(len(connection.queries))
            return Response(data)
        except Proyecto.DoesNotExist:
            raise ValidationError('ProyectoID does not exist')
    

class UserProyectoTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProyectoTypeSerializer
    queryset = UserProyectoType.objects.all()
    lookup_field = 'UserProyectoTypeID'


class ApproveCreateProyectoLegalViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckApproveInmueblesPermission,)
    serializer_class = ApproveCreateProyectoLegalSerializer
    queryset = Proyecto.objects.all()
    lookup_field = 'ProyectoID'

    def partial_update(self, request, ProyectoID):
        serializer = ApproveCreateProyectoLegalSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )
        if serializer.is_valid():
            resolution = serializer.validated_data.get("Resolution")
            if resolution:
                serializer.save()
                return Response({"proyecto": serializer.data,
                                 "detail": "Aprobación realizada con éxito"},
                                status=status.HTTP_200_OK)
            else:
                serializer.save()
                return Response({"proyecto": serializer.data,
                                 "detail": "Rechazo realizado con éxito"},
                                status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class ApproveCreateProyectoGerenciaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CheckMonitorProyectosPermission,)
    serializer_class = ApproveCreateProyectoGerenciaSerializer
    queryset = Proyecto.objects.all()
    lookup_field = 'ProyectoID'

    def partial_update(self, request, ProyectoID):
        serializer = ApproveCreateProyectoGerenciaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            resolution = serializer.validated_data.get("Resolution")
            if resolution:
                serializer.save()
                return Response({"proyecto": serializer.data,
                                 "detail": "Aprobación realizada con éxito"},
                                status=status.HTTP_200_OK)
            else:
                serializer.save()
                return Response({"proyecto": serializer.data,
                                 "detail": "Rechazo realizado con éxito"},
                                status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class CreateNotificationLegalUsersViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SendProyectoLegalSerializer
    queryset = Proyecto.objects.all()
    lookup_field = 'ProyectoID'

    def partial_update(self, request, ProyectoID):
        serializer = SendProyectoLegalSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"proyecto": serializer.data,
                             "detail": "Proyecto enviado a aprobación"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class CreateNotificationGerenciaUsersViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SendProyectoGerenciaSerializer
    queryset = Proyecto.objects.all()
    lookup_field = 'ProyectoID'

    def partial_update(self, request, ProyectoID):
        serializer = SendProyectoGerenciaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"proyecto": serializer.data,
                             "detail": "Proyecto enviado a aprobación"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)


class AddBorradorPromesaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AddBorradorPromesaSerializer
    queryset = Proyecto.objects.all()
    lookup_field = 'ProyectoID'

    def partial_update(self, request, ProyectoID):
        serializer = AddBorradorPromesaSerializer(
            self.get_object(), data=request.data,
            partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"proyecto": serializer.data,
                             "detail": "Borrador Promesa agregado con éxito"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_409_CONFLICT)
