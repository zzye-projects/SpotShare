from rest_framework import status, response, viewsets, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from ..models import Address
from ..serializers import AddressSerializer
from ..permissions import IsSuperAdminOrGET


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsSuperAdminOrGET]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = {
        'street': ['exact', 'icontains'],  
        'city': ['exact', 'icontains'],
        'state': ['exact', 'icontains'],
        'postal_code': ['exact'],
        'country': ['exact', 'icontains'],
    }
    ordering_fields = ['street', 'city', 'state', 'postal_code', 'country']

    def add_user_to_address(self, request, pk=None):
        address = get_object_or_404(Address, pk=pk)
        user = request.user
        add_users = request.data.get('users')

        if not add_users:
            return response.Response({'message':'No users to add.'}, status=status.HTTP_400_BAD_REQUEST)

        for user_pk in add_users:
            user = get_object_or_404(User, pk=user_pk)
            address.add_user(user)

        return response.Response({'message':'Users added to the address.'}, status=status.HTTP_200_OK)