from rest_framework.test import APITestCase
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from spot_share.models import Address, Parking
from django.contrib.auth.models import User, Group
from spot_share.serializers import ParkingSerializer

class ParkingTestCase(APITestCase):
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

        cls.lessor_user1 = User.objects.create_user(
            username='LessorUser1', 
            password='LessorUser1@123!'
        )
        cls.lessor_user2 = User.objects.create_user(
            username='LessorUser2', 
            password='LessorUser2@123!'
        )

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
        cls.address2.add_staff_user(cls.staff_user2)

        cls.today = timezone.now().date()
        cls.parking1 = Parking.objects.create(
            lessor=cls.lessor_user1,
            address=cls.address1,
            parking_unit='P1 U1',
            available_start=cls.today + timedelta(days=11),
            payment_amount = 100,
            payment_frequency = 'MONTHLY'
        )
        
        cls.parking2 = Parking.objects.create(
            lessor=cls.lessor_user2,
            address=cls.address2,
            parking_unit='P2 U2',
            available_start=cls.today + timedelta(days=12),
            available_end=cls.today + timedelta(days=22),
            payment_amount = 200,
            payment_frequency = 'ANNUALLY'
        )
        
    def test_list_parking(self):
        response = self.client.get(reverse('parking-list'))
        serializer = ParkingSerializer(
            Parking.objects.all(), 
            many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_parking(self):
        response = self.client.get(
            reverse('parking-detail', kwargs={'pk': self.parking1.pk}))

        serializer = ParkingSerializer(
            self.parking1, 
            many=False)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_fail_auth_post_parking(self):
        response = self.client.post(
            reverse('parking-list'),
            data={},
            format='json')
        
        self.assertEqual(response.status_code, 403)

    def test_fail_auth_staff_post_parking(self):
        payload = {
            'lessor': self.lessor_user1.pk,
            'address': self.address2.pk,
            'parking_unit': 'P2 U1',
            'available_start': self.today + timedelta(days=11),
            'available_end': self.today + timedelta(days=21),
            'status': 'ACTIVE',
            'payment_amount': 100,
            'payment_frequency': 'MONTHLY'
        }
        self.client.login(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        response = self.client.post(
            reverse('parking-list'),
            data=payload,
            format='json')
        
        self.assertEqual(response.status_code, 403)

    def test_post_parking(self):
        
        payload = {
            'lessor': self.lessor_user1.pk,
            'address': self.address2.pk,
            'parking_unit': 'P2 U1',
            'available_start': self.today + timedelta(days=11),
            'available_end': self.today + timedelta(days=21),
            'status': 'ACTIVE',
            'payment_amount': 300,
            'payment_frequency': 'WEEKLY'
        }
        self.client.login(
            username='LessorUser1', 
            password='LessorUser1@123!'
        )
        response = self.client.post(
            reverse('parking-list'),
            data=payload,
            format='json')

        self.assertEqual(response.status_code, 201)
        parking3 = get_object_or_404(Parking, parking_unit='P2 U1')
        self.assertEqual(parking3.lessor, self.lessor_user1)
        self.assertEqual(parking3.address, self.address2)
        self.assertEqual(parking3.available_start, self.today + timedelta(days=11))
        self.assertEqual(parking3.available_end, self.today + timedelta(days=21))
        self.assertEqual(parking3.status, 'DRAFT')
        self.assertEqual(parking3.payment_amount, 300)
        self.assertEqual(parking3.payment_frequency, 'WEEKLY')

    def test_fail_lessor_patch_parking(self):
        self.client.login(
            username='LessorUser1', 
            password='LessorUser1@123!'
        )
        response = self.client.patch(
            reverse('parking-detail', kwargs={'pk':self.parking2.pk}),
            data={},
            format='json')
        self.assertEqual(response.status_code, 403)

    def test_lessor_patch_parking(self):
        self.client.login(
            username='LessorUser1', 
            password='LessorUser1@123!'
        )
        payload = {
            'lessor': self.lessor_user1.pk,
            'address': self.address2.pk,
            'parking_unit': 'P1 U11',
            'available_start': self.today + timedelta(days=111),
            'available_end': self.today + timedelta(days=211),
            'status': 'ACTIVE',
            'payment_amount': 101,
            'payment_frequency': 'WEEKLY'
        }
        
        response = self.client.patch(
            reverse('parking-detail', kwargs={'pk':self.parking1.pk}),
            data=payload,
            format='json')
        self.assertEqual(response.status_code, 200)
        parking1 = get_object_or_404(Parking, pk=self.parking1.pk)
        self.assertEqual(parking1.lessor, self.lessor_user1)
        self.assertEqual(parking1.address, self.address1)
        self.assertEqual(parking1.parking_unit, 'P1 U11')
        self.assertEqual(parking1.available_start, self.today + timedelta(days=111))
        self.assertEqual(parking1.available_end, self.today + timedelta(days=211))
        self.assertEqual(parking1.status, 'DRAFT')
        self.assertEqual(parking1.payment_amount, 101)
        self.assertEqual(parking1.payment_frequency, 'WEEKLY')

    def test_fail_staff_patch_parking(self):
        self.client.login(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        response = self.client.patch(
            reverse('parking-detail', kwargs={'pk':self.parking2.pk}),
            data={},
            format='json')
        self.assertEqual(response.status_code, 403)

    def test_staff_patch_parking(self):
        self.client.login(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        payload = {
            'lessor': self.lessor_user1.pk,
            'address': self.address2.pk,
            'parking_unit': 'P1 U111',
            'available_start': self.today + timedelta(days=1111),
            'available_end': self.today + timedelta(days=2111),
            'status': 'ARCHIVED',
            'payment_amount': 102,
            'payment_frequency': 'ANNUALLY'
        }
        response = self.client.patch(
            reverse('parking-detail', kwargs={'pk':self.parking1.pk}),
            data=payload,
            format='json')
        
        self.assertEqual(response.status_code, 200)
        parking1 = get_object_or_404(Parking, pk=self.parking1.pk)
        self.assertEqual(parking1.lessor, self.lessor_user1)
        self.assertEqual(parking1.address, self.address1)
        self.assertEqual(parking1.parking_unit, 'P1 U111')
        self.assertEqual(parking1.available_start, self.today + timedelta(days=1111))
        self.assertEqual(parking1.available_end, self.today + timedelta(days=2111))
        self.assertEqual(parking1.status, 'ARCHIVED')
        self.assertEqual(parking1.payment_amount, 102)
        self.assertEqual(parking1.payment_frequency, 'ANNUALLY')

    def test_fail_put_parking(self):
        self.client.login(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        response = self.client.put(
            reverse('parking-detail', kwargs={'pk':self.parking1.pk}),
            data={},
            format='json')
        self.assertEqual(response.status_code, 405)
    
    def test_fail_lessor_remove_parking(self):
        self.client.login(
            username='LessorUser1', 
            password='LessorUser1@123!'
        )
        response = self.client.delete(
            reverse('parking-detail', kwargs={'pk': self.parking2.pk}))
        
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Parking.objects.filter(pk=self.parking2.pk).exists())

    def test_lessor_remove_parking(self):
        self.client.login(
            username='LessorUser1', 
            password='LessorUser1@123!'
        )

        response = self.client.delete(
            reverse('parking-detail', kwargs={'pk': self.parking1.pk}))
        
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Parking.objects.filter(pk=self.parking1.pk).exists())

    def test_fail_staff_remove_parking(self):
        self.client.login(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        response = self.client.delete(
            reverse('parking-detail', kwargs={'pk': self.parking2.pk}))
        
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Parking.objects.filter(pk=self.parking2.pk).exists())
    
    def test_staff_remove_parking(self):
        self.client.login(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        response = self.client.delete(
            reverse('parking-detail', kwargs={'pk': self.parking1.pk}))
        
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Parking.objects.filter(pk=self.parking1.pk).exists())

