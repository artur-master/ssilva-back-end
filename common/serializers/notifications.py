from common.models import Notification
from users.serializers.users import ListResponsableSerializer
from rest_framework import serializers


# Serializador para el modelo Notification

class NotificationSerializer(serializers.ModelSerializer):
    NotificationName = serializers.CharField(
        source='NotificationTypeID.Name',
        read_only=True
    )
    TableName = serializers.CharField(
        source='NotificationTypeID.TableName',
        read_only=True
    )
    RedirectRouteName = serializers.CharField(
        source='NotificationTypeID.RedirectRouteName',
        read_only=True
    )

    class Meta:
        model = Notification
        fields = (
            'NotificationID',
            'NotificationName',
            'TableName',
            'CreationDate',
            'Message',
            'RedirectRouteID',
            'RedirectRouteName'
        )


# Serializador para Notificaciones en proyecto


class NotificationRetrieveProyectoSerializer(serializers.ModelSerializer):
    NotificationName = serializers.CharField(
        source='NotificationTypeID.Name',
        read_only=True
    )
    TableName = serializers.CharField(
        source='NotificationTypeID.TableName',
        read_only=True
    )
    RedirectRouteName = serializers.CharField(
        source='NotificationTypeID.RedirectRouteName',
        read_only=True
    )
    Users = ListResponsableSerializer(
        source='UserID',
        many=True
    )

    class Meta:
        model = Notification
        fields = (
            'NotificationID',
            'NotificationName',
            'TableName',
            'CreationDate',
            'Message',
            'RedirectRouteID',
            'RedirectRouteName',
            'Users')
