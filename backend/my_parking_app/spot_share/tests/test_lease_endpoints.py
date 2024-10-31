from rest_framework.test import APITestCase
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from spot_share.models import Address, Parking, Lease, Vehicle
from django.contrib.auth.models import User, Group
from spot_share.serializers import LeaseSerializer, LeaseListSerializer

class LeaseTestCase(APITestCase):
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

        cls.tenant_user1 = User.objects.create_user(
            username='TenantUser1', 
            password='TenantUser1@123!'
        )
        cls.vehicle1 = Vehicle.objects.create(
            owner=cls.tenant_user1, 
            make='make1',
            model='model1',
            colour='colour1',
            license_plate='license1'
        )
        cls.tenant_user2 = User.objects.create_user(
            username='TenantUser2', 
            password='TenantUser2@123!'
        )
        cls.vehicle2 = Vehicle.objects.create(
            owner=cls.tenant_user2, 
            make='make2',
            model='model2',
            colour='colour2',
            license_plate='license2'
        )
        cls.lease1 = Lease.objects.create(
            parking=cls.parking1,
            vehicle=cls.vehicle1,
            lessor=cls.lessor_user1,
            tenant=cls.tenant_user1,
            start_date = cls.today + timedelta(days=11+1),
            end_date = cls.today + timedelta(days=11+30),
            payment_frequency='ANNUALLY',
            payment_type='CREDIT',
            payment_details='payment details 1',
            payment_amount=100
        )

        cls.lease2 = Lease.objects.create(
            parking=cls.parking2,
            vehicle=cls.vehicle2,
            lessor=cls.lessor_user2,
            tenant=cls.tenant_user2,
            start_date = cls.today + timedelta(days=12+1),
            end_date = cls.today + timedelta(days=12+10),
            payment_frequency='WEEKLY',
            payment_type='DEBIT',
            payment_details='payment details 2',
            payment_amount=200
        )

    def test_list_leases(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        response = self.client.get(reverse('lease-list'))
        self.assertEqual(response.status_code, 200)

        serializer = LeaseListSerializer(Lease.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)

    def test_staff_list_leases(self):
        self.client.login(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        
        response = self.client.get(reverse('lease-list'))
        self.assertEqual(response.status_code, 200)

        serializer = LeaseListSerializer(
            Lease.objects.filter(parking__address__in=self.staff_user1.addresses.all()), 
            many=True)
        self.assertEqual(response.data, serializer.data)

    def test_lessor_list_leases(self):
        self.client.login(
            username='LessorUser1', 
            password='LessorUser1@123!'
        )
        
        response = self.client.get(reverse('lease-list'))
        self.assertEqual(response.status_code, 200)

        serializer = LeaseListSerializer(
            Lease.objects.filter(lessor=self.lessor_user1), many=True)
        self.assertEqual(response.data, serializer.data)

    def test_tenant_list_leases(self):
        self.client.login(
            username='TenantUser2', 
            password='TenantUser2@123!'
        )
        
        response = self.client.get(reverse('lease-list'))
        self.assertEqual(response.status_code, 200)

        serializer = LeaseListSerializer(
            Lease.objects.filter(tenant=self.tenant_user2), many=True)
        self.assertEqual(response.data, serializer.data)

    def test_fail_auth_list_leases(self):
        response = self.client.get(reverse('lease-list'))
        self.assertEqual(response.status_code, 403)

    def test_lessor_retrieve_lease(self):
        self.client.login(
            username='LessorUser1', 
            password='LessorUser1@123!'
        )
        response = self.client.get(
            reverse('lease-detail', kwargs={'pk':self.lease1.pk}))
        self.assertEqual(response.status_code, 200)

        serializer = LeaseSerializer(self.lease1, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data['payment_amount'], '100.00')
        self.assertEqual(response.data['payment_details'], 'payment details 1')

    def test_fail_lessor_retrieve_lease(self):
        self.client.login(
            username='LessorUser1', 
            password='LessorUser1@123!'
        )
        response = self.client.get(
            reverse('lease-detail', kwargs={'pk':self.lease2.pk}))
        self.assertEqual(response.status_code, 404)

    def test_tenant_retrieve_lease(self):
        self.client.login(
            username='TenantUser2', 
            password='TenantUser2@123!'
        )
        response = self.client.get(
            reverse('lease-detail', kwargs={'pk':self.lease2.pk}))
        self.assertEqual(response.status_code, 200)

        serializer = LeaseSerializer(self.lease2, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data['payment_amount'], '200.00')
        self.assertEqual(response.data['payment_details'], 'payment details 2')

    def test_fail_tenant_retrieve_lease(self):
        self.client.login(
            username='TenantUser2', 
            password='TenantUser2@123!'
        )
        response = self.client.get(
            reverse('lease-detail', kwargs={'pk':self.lease1.pk}))
        self.assertEqual(response.status_code, 404)

    def test_staff_retrieve_lease(self):
        self.client.login(
            username='StaffUser2', 
            password='StaffUser2@123!'
        )
        response = self.client.get(
            reverse('lease-detail', kwargs={'pk':self.lease2.pk}))
        self.assertEqual(response.status_code, 200)

        expected_data = dict(LeaseSerializer(self.lease2, many=False).data)
        expected_data.pop('payment_details', None)
        expected_data.pop('payment_amount', None)
        self.assertEqual(response.data, expected_data)

    def test_fail_staff_retrieve_lease(self):
        self.client.login(
            username='TenantUser2', 
            password='TenantUser2@123!'
        )
        response = self.client.get(
            reverse('lease-detail', kwargs={'pk':self.lease1.pk}))
        self.assertEqual(response.status_code, 404)

    def test_fail_auth_retrieve_lease(self):
        response = self.client.get(
            reverse('lease-detail', kwargs={'pk':self.lease1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_tenant_create_lease(self):
        payload={
            'parking': self.parking1.pk,
            'vehicle': self.vehicle1.pk,
            'start_date': self.today + timedelta(days=11+1),
            'end_date': self.today + timedelta(days=11+30),
            'payment_frequency': 'WEEKLY',
            'payment_type': 'DEBIT',
            'payment_details': 'payment details 3',
            'payment_amount': 300
        }
        self.client.login(
            username='TenantUser1', 
            password='TenantUser1@123!'
        )

        response = self.client.post(
            reverse('lease-list'),
            data=payload,
            format='json'
        )
        lease = get_object_or_404(Lease, payment_details='payment details 3')
        comparison_pair = [
            [response.status_code, 201], 
            [lease.parking, self.parking1], 
            [lease.vehicle, self.vehicle1],
            [lease.lessor, self.lessor_user1], 
            [lease.tenant, self.tenant_user1],
            [lease.start_date, self.today + timedelta(days=11+1)], 
            [lease.end_date,self.today + timedelta(days=11+30)],
            [lease.payment_frequency, 'WEEKLY'], 
            [lease.payment_amount, 300], 
            [lease.payment_type, 'DEBIT']]
        for [item, expected_value] in comparison_pair: self.assertEqual(item, expected_value)

    def test_fail_tenant_create_lease(self):
        payload={
            'parking': self.parking1.pk,
            'vehicle': self.vehicle1.pk,
            'start_date': self.today + timedelta(days=11+1),
            'end_date': self.today + timedelta(days=11+30),
            'payment_frequency': 'WEEKLY',
            'payment_type': 'DEBIT',
            'payment_details': 'payment details 3',
            'payment_amount': 300
        }
        self.client.login(
            username='TenantUser2', 
            password='TenantUser2@123!'
        )

        response = self.client.post(
            reverse('lease-list'),
            data=payload,
            format='json'
        )
        self.assertEqual(response.status_code, 403)

    def test_fail_lessor_create_lease(self):
        payload={
            'parking': self.parking1.pk,
            'vehicle': self.vehicle1.pk,
            'start_date': self.today + timedelta(days=11+1),
            'end_date': self.today + timedelta(days=11+30),
            'payment_frequency': 'WEEKLY',
            'payment_type': 'DEBIT',
            'payment_details': 'payment details 3',
            'payment_amount': 300
        }
        self.client.login(
            username='LessorUser2', 
            password='LessorUser2@123!'
        )

        response = self.client.post(
            reverse('lease-list'),
            data=payload,
            format='json'
        )
        self.assertEqual(response.status_code, 403)

    def test_staff_create_lease(self):
        payload={
            'parking': self.parking1.pk,
            'vehicle': self.vehicle2.pk,
            'start_date': self.today + timedelta(days=11+1),
            'end_date': self.today + timedelta(days=11+30),
            'payment_frequency': 'WEEKLY',
            'payment_type': 'DEBIT',
            'payment_details': 'payment details 4',
            'payment_amount': 400
        }
        self.client.login(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        response = self.client.post(
            reverse('lease-list'),
            data=payload,
            format='json'
        )
        lease = get_object_or_404(Lease, payment_details='payment details 4')
        comparison_pair = [
            [response.status_code, 201], 
            [lease.parking, self.parking1], 
            [lease.vehicle, self.vehicle2],
            [lease.lessor, self.lessor_user1], 
            [lease.tenant, self.tenant_user2],
            [lease.start_date, self.today + timedelta(days=11+1)], 
            [lease.end_date,self.today + timedelta(days=11+30)],
            [lease.payment_frequency, 'WEEKLY'], 
            [lease.payment_amount, 400], 
            [lease.payment_type, 'DEBIT']]
        for [item, expected_value] in comparison_pair: self.assertEqual(item, expected_value)

    def test_fail_staff_create_lease(self):
        payload={
            'parking': self.parking2.pk,
            'vehicle': self.vehicle2.pk,
            'start_date': self.today + timedelta(days=11+1),
            'end_date': self.today + timedelta(days=11+30),
            'payment_frequency': 'WEEKLY',
            'payment_type': 'DEBIT',
            'payment_details': 'payment details 4',
            'payment_amount': 400
        }
        self.client.login(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        response = self.client.post(
            reverse('lease-list'),
            data=payload,
            format='json'
        )
        self.assertEqual(response.status_code, 403)
    def test_fail_auth_create_lease(self):
        payload={
            'parking': self.parking2.pk,
            'vehicle': self.vehicle2.pk,
            'start_date': self.today + timedelta(days=11+1),
            'end_date': self.today + timedelta(days=11+30),
            'payment_frequency': 'WEEKLY',
            'payment_type': 'DEBIT',
            'payment_details': 'payment details 4',
            'payment_amount': 400
        }
        response = self.client.post(
            reverse('lease-list'),
            data=payload,
            format='json'
        )
        self.assertEqual(response.status_code, 403)

    # all destroy
    # all partial update


    
