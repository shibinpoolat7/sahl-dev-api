"""
Serializers for vehicle APIs
"""
from rest_framework import serializers

from core.models import Vehicle,Customer,Agreement


class VehicleSerializer(serializers.ModelSerializer):
    """Serializer for vehicles."""

    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle_name', 'registration_no', 'daily_min_rate', 'monthly_min_rate','status']
        read_only_fields = ['id']

class VehicleDetailSerializer(VehicleSerializer):
    """Serializer for vehicle detail view."""

    class Meta(VehicleSerializer.Meta):
        fields = VehicleSerializer.Meta.fields + ['daily_max_rate','monthly_max_rate']

class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for customers."""

    class Meta:
        model = Customer
        fields = ['id', 'customer_name','customer_type', 'cr_id_no', 'customer_email', 'customer_mobile']
        read_only_fields = ['id']

class CustomerDetailSerializer(CustomerSerializer):
    """Serializer for customer detail view."""

    class Meta(CustomerSerializer.Meta):
        fields = CustomerSerializer.Meta.fields + ['customer_address', 'customer_phone', 'is_blocked']

class AgreementSerializer(serializers.ModelSerializer):
    """Serializer for Agreements."""

    class Meta:
        model = Agreement
        fields = ['id', 'rent_type', 'agreement_no', 'deposit_type', 'checkin_date', 'customer', 'vehicle']
        read_only_fields = ['id']

class AgreementDetailSerializer(AgreementSerializer):
    """Serializer for agreement detail view."""

    class Meta(AgreementSerializer.Meta):
        fields = AgreementSerializer.Meta.fields + ['external_customer_name', 'checkout_date']

class VehicleImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to vehicles."""

    class Meta:
        model = Vehicle
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}
