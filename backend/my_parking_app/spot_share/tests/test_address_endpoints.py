from rest_framework.test import APITestCase
from django.shortcuts import get_object_or_404
from django.urls import reverse

from spot_share.models import Address
from django.contrib.auth.models import User, Group
from spot_share.serializers import AddressSerializer


class AddressTestCase(APITestCase):
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
        cls.customer_user = User.objects.create_user(
            username='CustomerUser2', 
            password='CustomerUser2@123!'
        )
        group, created = Group.objects.get_or_create(name='Staff')
        cls.staff_user1.groups.add(group)
        cls.staff_user2.groups.add(group)

        cls.address1 = Address.objects.create(
            street = 'street1',
            street_no = 1, 
            city = 'city1',
            state = 'state1',
            postal_code = 'postal_code1',
            country = 'country1'
        )
        cls.address1.add_staff_user(cls.staff_user1)

        cls.address2 = Address.objects.create(
            street = 'street2',
            street_no = 2, 
            city = 'city2',
            state = 'state2',
            postal_code = 'postal_code2',
            country = 'country2',
        )
    
    def test_list_addresses(self):
        serializer = AddressSerializer(Address.objects.all(), many=True)
        response = self.client.get(reverse('address-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_details_address(self):
        serializer = AddressSerializer(self.address1)
        response = self.client.get(reverse('address-detail', kwargs={'pk': self.address1.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
    
    def test_post_address(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        payload = {
            'street': 'street3',
            'street_no': 3, 
            'city': 'city3',
            'state': 'state3',
            'postal_code': 'postal_code3',
            'country': 'country3',
        }
        response = self.client.post(
            reverse('address-list'), 
            data=payload, 
            format='json'
        )
        self.assertEqual(response.status_code, 201)

        address3 = Address.objects.filter(postal_code='postal_code3').first()
        self.assertEqual(address3.street, 'street3')
        self.assertEqual(address3.street_no, 3)
        self.assertEqual(address3.city, 'city3')
        self.assertEqual(address3.state, 'state3')
        self.assertEqual(address3.country, 'country3')

    def test_fail_auth_post_address(self):
        self.client.login(
            username='StaffUser', 
            password='StaffUser@123!'
        )
        response = self.client.post(
            reverse('address-list'), 
            data={}, 
            format='json'
        )
        self.assertEqual(response.status_code, 403)

    def test_put_address(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        payload = {
            'street': 'street11',
            'street_no': 11, 
            'city': 'city11',
            'state': 'state11',
            'postal_code': 'postal_code11',
            'country': 'country11',
        }
        response = self.client.put(
            reverse('address-detail', kwargs={'pk': self.address1.pk}), 
            data=payload, 
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        address = get_object_or_404(Address, pk=self.address1.pk)
        self.assertEqual(address.street, 'street11')
        self.assertEqual(address.street_no, 11)
        self.assertEqual(address.city, 'city11')
        self.assertEqual(address.state, 'state11')
        self.assertEqual(address.postal_code, 'postal_code11')
        self.assertEqual(address.country, 'country11')

    def test_fail_auth_put_address(self):
        self.client.login(
            username='StaffUser', 
            password='StaffUser@123!'
        )
        response = self.client.put(
            reverse('address-detail', kwargs={'pk': self.address1.pk}), 
            data={}, 
            format='json'
        )
        self.assertEqual(response.status_code, 403)

    def test_patch_address(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        payload = {
            'street': 'street11',
            'street_no': 11
        }
        response = self.client.patch(
            reverse('address-detail', kwargs={'pk': self.address1.pk}), 
            data=payload, 
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        address = get_object_or_404(Address, pk=self.address1.pk)
        self.assertEqual(address.street, 'street11')
        self.assertEqual(address.street_no, 11)
        self.assertEqual(address.city, 'city1')
        self.assertEqual(address.state, 'state1')
        self.assertEqual(address.postal_code, 'postal_code1')
        self.assertEqual(address.country, 'country1')

    def test_fail_auth_patch_address(self):
        self.client.login(
            username='StaffUser', 
            password='StaffUser@123!'
        )
        response = self.client.patch(
            reverse('address-detail', kwargs={'pk': self.address1.pk}), 
            data={}, 
            format='json'
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_address(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        response = self.client.delete(
            reverse('address-detail', kwargs={'pk': self.address1.pk}), 
            format='json'
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Address.objects.filter(pk=self.address1.pk).exists())

    def test_fail_auth_delete_address(self):
        self.client.login(
            username='StaffUser', 
            password='StaffUser@123!'
        )
        response = self.client.delete(
            reverse('address-detail', kwargs={'pk': self.address1.pk}), 
            data={}, 
            format='json'
        )
        self.assertEqual(response.status_code, 403)  
        self.assertTrue(Address.objects.filter(pk=self.address1.pk).exists())
      
    def test_add_staff_user(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        response = self.client.post(
            reverse('add-staff-user', kwargs={'pk': self.address2.pk}), 
            data={'users': [self.staff_user1.pk, self.staff_user2.pk]},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.address2.staff_users.all()), 2)
        self.assertTrue(self.address2.staff_users.filter(pk=self.staff_user1.pk).exists())
        self.assertTrue(self.address2.staff_users.filter(pk=self.staff_user2.pk).exists())
    
    def test_fail_auth_add_staff_user(self):
        self.client.login(
            username='StaffUser', 
            password='StaffUser@123!'
        )
        response = self.client.post(
            reverse('add-staff-user', kwargs={'pk': self.address2.pk}), 
            data={'users': [self.staff_user1.pk, self.staff_user2.pk]}, 
            format='json'
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(self.address2.staff_users.all()), 0)

    def test_remove_staff_user(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        response = self.client.delete(
            reverse('remove-staff-user', kwargs={'pk': self.address1.pk}), 
            data={'users': [self.staff_user1.pk, self.staff_user2.pk]},
            format='json'
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(self.address1.staff_users.all()), 0)
    
    def test_fail_auth_remove_staff_user(self):
        self.client.login(
            username='StaffUser', 
            password='StaffUser@123!'
        )
        response = self.client.delete(
            reverse('remove-staff-user', kwargs={'pk': self.address1.pk}), 
            data={'users': [self.staff_user1.pk, self.staff_user2.pk]}, 
            format='json'
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(self.address1.staff_users.all()), 1)


