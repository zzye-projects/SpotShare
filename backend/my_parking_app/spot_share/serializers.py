from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User, Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'groups']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'street_no', 'city', 'state', 'postal_code', 'country']

class ParkingSerializer(serializers.ModelSerializer):
    lessor = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        many=False)

    class Meta:
        model = Parking
        fields =  '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=False)
    
    class Meta:
        model = Vehicle
        fields = '__all__'

class LeaseSerializer(serializers.ModelSerializer):
    lessor = serializers.PrimaryKeyRelatedField(
        read_only=True,
        many=False)
    tenant = serializers.PrimaryKeyRelatedField(
        read_only=True,
        many=False)
    
    class Meta:
        model = Lease
        fields = '__all__'

class LeaseListSerializer(serializers.ModelSerializer):
    lessor = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        many=False)
    tenant = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        many=False)
    parking = serializers.PrimaryKeyRelatedField(
        queryset = Parking.objects.all(),
        many = False
    )
    vehicle = serializers.PrimaryKeyRelatedField(
        queryset = Vehicle.objects.all(),
        many = False
    )
    
    class Meta:
        model = Lease
        fields = ['parking', 'vehicle', 'lessor', 'lessor_approved', 
                  'tenant', 'tenant_approved', 'start_date', 'end_date', 'staff_approved']
    