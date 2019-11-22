from ventas.models.conditions import Condition
from rest_framework import serializers


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ('ConditionID', 'Description', 'IsImportant', 'IsApprove')


class ApproveConditionSerializer(serializers.ModelSerializer):
    ConditionID = serializers.CharField(
        write_only=True
    )
    IsApprove = serializers.BooleanField(
        write_only=True
    )

    class Meta:
        model = Condition
        fields = ('ConditionID', 'IsApprove')


class CreateConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ('Description',)


