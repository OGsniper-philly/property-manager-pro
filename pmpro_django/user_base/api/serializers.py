from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user_base.models import Property, Tenant


class PropertySerializer(ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class TenantSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    property = PropertySerializer()

    class Meta:
        model = Tenant
        fields = '__all__'
