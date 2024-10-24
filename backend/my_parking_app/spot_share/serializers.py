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

# class VehicleSerializer(serializers.ModelSerializer):
#     owner = UserSerializer(read_only=True)
#     owner_id = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(),
#         write_only=True)
    
#     class Meta:
#         model = Vehicle
#         fields = '__all__'
