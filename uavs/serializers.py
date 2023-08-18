from django.utils import timezone
from datetime import datetime
from rest_framework import serializers
from uavs.models import UAVCategory, UAV, RentedUAV


class UAVCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the UAVCategory model.
    """
    class Meta:
        model = UAVCategory
        fields = "__all__"


class UAVSerializer(serializers.ModelSerializer):
    """
    Serializer for the UAV model.

    Serializes the following fields:
    - id
    - brand
    - model
    - category
    - is_rental
    - weight
    """
    class Meta:
        model = UAV
        fields = ["id", "brand", "model", "category", "is_rental", "weight"]


class RentUAVSerializer(serializers.Serializer):
    """
    Serializer for renting a UAV.

    Fields:
    - uav_id: CharField, required
    - start_date: DateField, required
    - end_date: DateField, required

    Methods:
    - validate_start_date: Validates that the start date is not before the current date.
    - validate_end_date: Validates that the end date is not before the current date.
    - validate: Validates that the start date is not after the end date.
    """
    uav_id = serializers.CharField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    def validate_start_date(self, value):
        if value < datetime.now().date():
            raise serializers.ValidationError(
                "The start date cannot be before the current date"
            )
        return value

    def validate_end_date(self, value):
        if value < datetime.now().date():
            raise serializers.ValidationError(
                "The end date cannot be before the current date"
            )
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["start_date"] > attrs["end_date"]:
            raise serializers.ValidationError(
                "The start date cannot be after the end date"
            )
        return attrs


class RentedUAVSerializer(serializers.ModelSerializer):
    """
    Serializer for the RentedUAV model.
    """
    class Meta:
        model = RentedUAV
        fields = "__all__"
