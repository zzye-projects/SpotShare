
from rest_framework.test import APITestCase
from django.shortcuts import get_object_or_404
from django.urls import reverse

from spot_share.models import Vehicle
from django.contrib.auth.models import User, Group
from spot_share.serializers import VehicleSerializer

class VehicleTestCase(APITestCase):
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
        group, created = Group.objects.get_or_create(name='Staff')
        cls.staff_user1.groups.add(group)

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
    def test_fail_auth_list_vehicles(self):
        response = self.client.get(reverse('vehicle-list'))
        self.assertEqual(response.status_code, 403)

    def test_fail_staff_list_vehicles(self):
        self.client.login(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        response = self.client.get(reverse('vehicle-list'))
        self.assertEqual(response.status_code, 403)

    def test_owner_list_vehicles(self):
        self.client.login(
            username='TenantUser1', 
            password='TenantUser1@123!'
        )
        response = self.client.get(reverse('vehicle-list'))
        serializer = VehicleSerializer(
            Vehicle.objects.filter(owner=self.tenant_user1), 
            many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_super_list_vehicles(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        response = self.client.get(reverse('vehicle-list'))
        serializer = VehicleSerializer(
            Vehicle.objects.all(), 
            many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_owner_retrieve(self):
        self.client.login(
            username='TenantUser1', 
            password='TenantUser1@123!'
        )
        response = self.client.get(
            reverse('vehicle-detail',
            kwargs= {'pk': self.vehicle1.pk}))
        serializer = VehicleSerializer(
            self.vehicle1, 
            many=False)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_fail_owner_retrieve(self):
        self.client.login(
            username='TenantUser1', 
            password='TenantUser1@123!'
        )
        response = self.client.get(
            reverse('vehicle-detail',
            kwargs= {'pk': self.vehicle2.pk}))
        self.assertEqual(response.status_code, 404)

    def test_fail_auth_retrieve(self):
        response = self.client.get(
            reverse('vehicle-detail',
            kwargs= {'pk': self.vehicle2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_staff_retrieve(self):
        self.client.login(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        response = self.client.get(
            reverse('vehicle-detail',
            kwargs= {'pk': self.vehicle1.pk}))
        serializer = VehicleSerializer(
            self.vehicle1, 
            many=False)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_user_create_vehicle(self):
        self.client.login(
            username='TenantUser1', 
            password='TenantUser1@123!'
        )
        payload={
            'owner': self.tenant_user2.pk, 
            'make': 'make11',
            'model':'model11',
            'colour':'colour11',
            'license_plate':'license11'
        }
        response = self.client.post(
            reverse('vehicle-list'),
            data=payload,
            format='json')
        self.assertEqual(response.status_code, 201)
        vehicle = get_object_or_404(Vehicle, license_plate='license11')
        self.assertEqual(vehicle.owner, self.tenant_user1)
        self.assertEqual(vehicle.make, 'make11')
        self.assertEqual(vehicle.model, 'model11')
        self.assertEqual(vehicle.colour, 'colour11')

    def test_fail_auth_create_vehicle(self):
        response = self.client.post(
            reverse('vehicle-list'),
            data={},
            format='json')
        self.assertEqual(response.status_code, 403)

    def test_fail_staff_create_vehicle(self):
        self.client.login(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        response = self.client.post(
            reverse('vehicle-list'),
            data={},
            format='json')
        self.assertEqual(response.status_code, 403)

    def test_owner_update(self):
        self.client.login(
            username='TenantUser1', 
            password='TenantUser1@123!'
        )
        payload={
            'owner': self.tenant_user2.pk, 
            'make': 'make12',
            'model':'model12',
            'colour':'colour12',
            'license_plate':'license12'
        }
        response = self.client.patch(
            reverse('vehicle-detail', kwargs={'pk':self.vehicle2.pk}),
            data=payload,
            format='json')
        self.assertEqual(response.status_code, 404)

        response = self.client.patch(
            reverse('vehicle-detail', kwargs={'pk':self.vehicle1.pk}),
            data=payload,
            format='json')
        self.assertEqual(response.status_code, 200)
        vehicle = get_object_or_404(Vehicle, pk=self.vehicle1.pk)
        self.assertEqual(vehicle.owner, self.tenant_user1)
        self.assertEqual(vehicle.make, 'make12')
        self.assertEqual(vehicle.model, 'model12')
        self.assertEqual(vehicle.colour, 'colour12')
        self.assertEqual(vehicle.license_plate, 'license12')

    def test_super_update(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        payload={
            'owner': self.tenant_user1.pk, 
            'make': 'make22',
            'model':'model22',
            'colour':'colour22',
            'license_plate':'license22'
        }
        response = self.client.patch(
            reverse('vehicle-detail', kwargs={'pk':self.vehicle2.pk}),
            data=payload,
            format='json')
        self.assertEqual(response.status_code, 200)
        vehicle = get_object_or_404(Vehicle, pk=self.vehicle2.pk)
        self.assertEqual(vehicle.owner, self.tenant_user1)
        self.assertEqual(vehicle.make, 'make22')
        self.assertEqual(vehicle.model, 'model22')
        self.assertEqual(vehicle.colour, 'colour22')
        self.assertEqual(vehicle.license_plate, 'license22')

    def test_fail_auth_update(self):
        response = self.client.patch(
            reverse('vehicle-detail', kwargs={'pk':self.vehicle2.pk}),
            data={},
            format='json')
        self.assertEqual(response.status_code, 403)

    def test_fail_staff_update(self):
        self.client.login(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        response = self.client.patch(
            reverse('vehicle-detail', kwargs={'pk':self.vehicle2.pk}),
            data={},
            format='json')
        self.assertEqual(response.status_code, 403)

    def test_user_destroy_vehicle(self):
        self.client.login(
            username='TenantUser1', 
            password='TenantUser1@123!'
        )
        response = self.client.delete(
            reverse('vehicle-detail', kwargs={'pk':self.vehicle2.pk}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Vehicle.objects.filter(pk=self.vehicle2.pk).exists())

        response = self.client.delete(
            reverse('vehicle-detail', kwargs={'pk':self.vehicle1.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Vehicle.objects.filter(pk=self.vehicle1.pk).exists())

    def test_super_destroy_vehicle(self):
        self.client.login(
            username='SuperUser', 
            password='SuperUser@123!'
        )
        response = self.client.delete(
            reverse('vehicle-detail', kwargs={'pk':self.vehicle2.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Vehicle.objects.filter(pk=self.vehicle2.pk).exists())

    def test_fail_staff_detroy_vehicle(self):
        self.client.login(
            username='StaffUser1', 
            password='StaffUser1@123!'
        )
        response = self.client.delete(
            reverse('vehicle-detail', kwargs={'pk':self.vehicle1.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Vehicle.objects.filter(pk=self.vehicle1.pk).exists())

    def test_fail_auth_destroy_vehicle(self):
        response = self.client.delete(
            reverse('vehicle-detail', kwargs={'pk':self.vehicle1.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Vehicle.objects.filter(pk=self.vehicle1.pk).exists())

