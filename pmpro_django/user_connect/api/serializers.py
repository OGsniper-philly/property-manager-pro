from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user_base.api.serializers import PropertySerializer, TenantSerializer
from user_connect.models import Invitation


class InvitationSerializer(ModelSerializer):
    landlord_username = serializers.CharField(source='property.landlord.user.username')
    landlord_first_name = serializers.CharField(source='property.landlord.user.first_name')
    landlord_last_name = serializers.CharField(source='property.landlord.user.last_name')

    tenant = TenantSerializer()

    property = PropertySerializer()

    class Meta:
        model = Invitation
        fields = '__all__'
