from rest_framework import status, response, viewsets, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Lease, Parking, Vehicle
from ..serializers import LeaseSerializer, LeaseListSerializer
from ..permissions import LeasePermissions
from django.db.models import Q

class LeaseViewSet(viewsets.ModelViewSet):
    permission_classes = [LeasePermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    http_method_names = ['get', 'post', 'patch', 'delete']

    filterset_fields = {
        'parking': ['exact'],
        'vehicle': ['exact'],
        'lessor': ['exact'],  
        'lessor_approved': ['exact'],
        'tenant': ['exact'],  
        'tenant_approved': ['exact'],
        'start_date': ['gte'],
        'end_date': ['lte'],
        'staff_approved': ['exact'],
    }
    ordering_fields = ['parking', 'vehicle', 'start_date', 'end_date']

    def get_serializer_class(self):
        if self.action == 'list':
            return LeaseListSerializer
        return LeaseSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Lease.objects.all()
        elif user.groups.filter(name='Staff').exists():
            return Lease.objects.filter(parking__address__in=user.addresses.all())
        return Lease.objects.filter(Q(lessor=user) | Q(tenant=user))

    def create(self, request, *args, **kwargs):
        data, user = request.data, request.user
        parking = get_object_or_404(Parking, pk=data['parking'])
        vehicle = get_object_or_404(Vehicle, pk=data['vehicle'])
        
        if user not in (parking.lessor, vehicle.owner) and \
            not user.addresses.filter(pk=parking.address.pk).exists():
            return response.Response(
                {'message': 'You have a tenant, lessor, or staff on this lease.'}, 
                status=status.HTTP_403_FORBIDDEN)
        
        data['lessor'] = parking.lessor.pk
        data['tenant'] = vehicle.owner.pk

        data.pop('lessor_approved', None)
        data.pop('tenant_approved', None)
        data.pop('status', None)

        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        response = super().retrieve(request, *args, **kwargs)

        if user.pk not in (response.data['lessor'], response.data['tenant']):
            response.data.pop('payment_amount', None)
            response.data.pop('payment_details', None)

        return response
    
    def partial_update(self, request, *args, **kwargs):
        lease, user = self.get_object(), request.user
        reset_fields = {'staff_approved': 'DRAFT', 'lessor_approved': 'PENDING', 
                        'tenant_approved': 'PENDING'}
        if lease.tenant == user:
            del reset_fields['tenant_approved']
        if lease.lessor == user: 
            del reset_fields['lessor_approved']
        if lease.parking.address in user.address.all():
            del reset_fields['staff_approved']

        for (key, value) in reset_fields.items():
            request.data[key] = value

        return super().partial_update(request, *args, **kwargs)