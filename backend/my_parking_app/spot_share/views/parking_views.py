from rest_framework import status, response, viewsets, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from ..models import Parking
from ..serializers import ParkingSerializer
from ..permissions import IsOwnerStaffAdminSuperOrGETOrPOST

class ParkingViewSet(viewsets.ModelViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [IsOwnerStaffAdminSuperOrGETOrPOST]
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
        request.data.pop('status', None)
        return super().create(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        instance, user = self.get_object(), request.user

        if not user.is_superuser and not user.is_staff and \
            not instance.address.staff_users.filter(pk=user.pk).exists():
            request.data['status'] = 'DRAFT'
        request.data.pop('lessor', None)
        request.data.pop('address', None)

        return super().partial_update(request, *args, **kwargs)