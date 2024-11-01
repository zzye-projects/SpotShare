from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from ..serializers import UserSerializer
from ..permissions import IsSuperAdminPermissions


class StaffUserView(APIView):
    permission_classes = [IsSuperAdminPermissions]
    
    def get(self, request):
        users = User.objects.filter(groups__name='Staff')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
    def post(self, request):
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, pk=user_id)

        group = get_object_or_404(Group, name='Staff')
        user.groups.add(group)

        user.save()
        return Response({'message': f'User {user_id} added to the Staff group'}, 
                        status=status.HTTP_201_CREATED)
    
class SingleStaffUserView(APIView):
    permission_classes = [IsSuperAdminPermissions]

    def delete(self, request, pk):
        group = get_object_or_404(Group, name='Staff')

        user = get_object_or_404(User, pk=pk)
        user.groups.remove(group)
        user.save()

        return Response({'message': f'Removed user id {pk} from Staff group'},
                        status=status.HTTP_200_OK)

