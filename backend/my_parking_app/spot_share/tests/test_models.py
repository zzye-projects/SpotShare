from django.test import TestCase
from spot_share.models import *
from django.contrib.auth.models import User, Group

class VehicleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        lessor_group, created = Group.objects.get_or_create(name='Lessor')
        renter_group, created = Group.objects.get_or_create(name='Renter')

        cls.renter_user = User.objects.create(
            username='RenterUser', 
            password='RU1@123!'
        )
        cls.renter_user.groups.add(renter_group)

    def test_vehicle_creation(self):
        vehicle1 = Vehicle.objects.create(
            owner=self.renter_user, 
            make='make1',
            model='model1',
            colour='colour1',
            license_plate='license1'
        )
        self.assertEqual(vehicle1.owner, self.renter_user)
        self.assertEqual(vehicle1.make, 'make1')
        self.assertEqual(vehicle1.model, 'model1')
        self.assertEqual(vehicle1.colour, 'colour1')
        self.assertEqual(vehicle1.license_plate, 'license1')

