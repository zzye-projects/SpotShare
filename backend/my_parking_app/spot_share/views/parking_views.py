from rest_framework import status, response, viewsets, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Parking, Address
from ..serializers import ParkingSerializer
from ..permissions import ParkingPermissions

class ParkingViewSet(viewsets.ModelViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [ParkingPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    http_method_names = ['get', 'post', 'patch', 'delete']

    filterset_fields = {
        'lessor': ['exact'],  
        'address': ['exact'],
        'parking_unit': ['exact', 'icontains'],
        'available_start': ['gte'],
        'available_end': ['lte'],
        'status': ['exact', 'icontains']
    }
    ordering_fields = ['address', 'available_start']
    
    def create(self, request, *args, **kwargs):
        user = request.user
        address = get_object_or_404(Address, pk=request.data.get('address'))

        if user.groups.filter(name='Staff').exists() and \
            not address.staff_users.filter(pk=user.pk).exists():
            return response.Response(
                {'message': 'Only staff users associated to the address can create associated parking'}, 
                status=status.HTTP_403_FORBIDDEN)
        
        request.data.pop('status', None)
        return super().create(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        if self.get_object().lessor == request.user:
            request.data['status'] = 'DRAFT'
        request.data.pop('lessor', None)
        request.data.pop('address', None)

        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance, user = self.get_object(), request.user

        if user.groups.filter(name='Staff').exists() and \
            not instance.address.staff_users.filter(pk=user.pk).exists():
            return response.Response(
                {'message': 'Only staff users associated to the address can delete associated parking'}, 
                status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)