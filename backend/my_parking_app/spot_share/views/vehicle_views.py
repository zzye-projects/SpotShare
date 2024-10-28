from rest_framework import status, response, viewsets, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Vehicle
from ..serializers import VehicleSerializer
from ..permissions import VehiclePermissions

class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [VehiclePermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    http_method_names = ['get', 'post', 'patch', 'delete']


    filterset_fields = {
        'owner': ['exact'],  
        'make': ['exact', 'icontains'],
        'model': ['exact', 'icontains'],
        'colour': ['exact', 'icontains'],
        'license_plate': ['exact', 'icontains'],
    }
    ordering_fields = ['owner', 'make', 'model', 'colour', 'license_plate']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff or \
            user.groups.filter(name='Staff').exists():
            return Vehicle.objects.all()
        return Vehicle.objects.filter(owner=user)
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser and not user.is_staff:
            request.data['owner'] = user.pk
        return super().create(request, *args, **kwargs)        
    
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        if not user.is_superuser and not user.is_staff:
            request.data.pop('owner', None)
        return super().partial_update(request, *args, **kwargs)