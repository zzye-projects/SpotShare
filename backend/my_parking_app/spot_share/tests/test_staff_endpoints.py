from rest_framework.test import APITestCase
from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.contrib.auth.models import User, Group
from spot_share.serializers import UserSerializer

class StaffTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_user = User.objects.create_superuser(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        cls.staff_user1 = User.objects.create_user(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        cls.staff_user2 = User.objects.create_user(
            username='StaffUser2', 
            password='StaffUser2@123!'
        )
        group, created = Group.objects.get_or_create(name='Staff')
        cls.staff_user1.groups.add(group)
        cls.staff_user2.groups.add(group)

        cls.staff_user3 = User.objects.create_user(
            username='StaffUser3', 
            password='StaffUser3@123!'
        )
    
    def test_list_staff(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        response = self.client.get(reverse('staff-list'))
        self.assertEqual(response.status_code, 200)
        
        serializer = UserSerializer(User.objects.filter(groups__name='Staff'), many=True)
        self.assertEqual(response.data, serializer.data)

    def test_fail_auth_list_staff(self):
        self.client.login(
            username='StaffUser2', 
            password='StaffUser2@123!'
        )
        response = self.client.get(reverse('staff-list'))
        self.assertEqual(response.status_code, 403)

    def test_add_staff(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        response = self.client.post(
            reverse('staff-list'),
            data = {'user_id': self.staff_user3.pk},
            format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.staff_user3.groups.filter(name='Staff').exists())

    def test_fail_auth_add_staff(self):
        self.client.login(
            username='StaffUser2', 
            password='StaffUser2@123!'
        )
        response = self.client.post(
            reverse('staff-list'),
            data = {'user_id': self.staff_user3.pk},
            format='json')
        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.staff_user3.groups.filter(name='Staff').exists())

    def test_remove_staff(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        response = self.client.delete(
            reverse('staff-detail'), kwargs={'pk': self.staff_user3.pk})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.staff_user3.groups.filter(name='Staff').exists())

    def test_fail_auth_remove_staff(self):
        self.client.login(
            username='StaffUser2', 
            password='StaffUser2@123!'
        )
        response = self.client.(
            reverse('staff-detail'), kwargs={'pk': self.staff_user3.pk})

        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.staff_user3.groups.filter(name='Staff').exists())

