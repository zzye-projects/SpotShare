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

    def change_user(self, request, change_type, pk):
        address = get_object_or_404(Address, pk=pk)
        users = request.data.get('users')

        if not users:
            return response.Response({'message':f'No users to {change_type}.'}, status=status.HTTP_400_BAD_REQUEST)

        for user_pk in users:
            user = get_object_or_404(User, pk=user_pk)
            if change_type == 'add':
                address.add_user(user)
            else:
                address.users.remove(user) 

        status_code = status.HTTP_200_OK if change_type == 'add' else status.HTTP_204_NO_CONTENT
        message = 'Users added to address' if change_type == 'add' else 'Users removed from address'
        return response.Response({'message': message}, status=status_code)
    
    def add_user(self, request, pk=None):
        return self.change_user(request, 'add', pk)
    
    def remove_user(self, request, pk=None):
        return self.change_user(request, 'remove', pk)