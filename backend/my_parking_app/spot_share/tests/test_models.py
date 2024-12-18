from django.test import TestCase
from spot_share.models import *
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import timedelta

class VehicleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tenant_user = User.objects.create(
            username='TenantUser', 
            password='TU1@123!'
        )

    def test_vehicle_creation(self):
        vehicle = Vehicle.objects.create(
            owner=self.tenant_user, 
            make='make1',
            model='model1',
            colour='colour1',
            license_plate='license1'
        )
        self.assertEqual(vehicle.owner, self.tenant_user)
        self.assertEqual(vehicle.make, 'make1')
        self.assertEqual(vehicle.model, 'model1')
        self.assertEqual(vehicle.colour, 'colour1')
        self.assertEqual(vehicle.license_plate, 'license1')

class AddressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff_user = User.objects.create_user(
            username='StaffUser', 
            password='StaffUser@123!'
        )
        group, created = Group.objects.get_or_create(name='Staff')
        cls.staff_user.groups.add(group)
        
        cls.address = Address.objects.create(
            street = 'street1',
            street_no = 1, 
            city = 'city1',
            state = 'state1',
            postal_code = 'postal_code1',
            country = 'country1',
        )
        cls.address.add_staff_user(cls.staff_user)

    def test_address_creation(self):
        self.assertEqual(self.address.street, 'street1')
        self.assertEqual(self.address.street_no, 1)
        self.assertEqual(self.address.city, 'city1')
        self.assertEqual(self.address.state, 'state1')
        self.assertEqual(self.address.postal_code, 'postal_code1')
        self.assertEqual(self.address.country, 'country1')
        self.assertIn(self.staff_user, self.address.staff_users.all())

    def test_fail_add_user(self):
        user = User.objects.create_user(
            username='User', 
            password='User@123!'
        )
        with self.assertRaises(ValidationError) as context:
            self.address.add_staff_user(user)
        self.assertIn(f'{user.username} is not Staff user. Only staff can be associated to an address.',
                      str(context.exception))

class ParkingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.address = Address.objects.create(
            street = 'street1',
            street_no = 1, 
            city = 'city1',
            state = 'state1',
            postal_code = 'postal_code1',
            country = 'country1',
        )
        cls.lessor_user = User.objects.create(
            username='LessorUser', 
            password='LU1@123!'
        )

    def test_parking_creation(self):
        today = timezone.now().date()
        parking = Parking.objects.create(
            lessor=self.lessor_user,
            address=self.address,
            parking_unit='P1 U1',
            available_start=today,
            payment_amount = 100,
            payment_frequency = 'MONTHLY')
        
        self.assertEqual(parking.lessor, self.lessor_user)
        self.assertEqual(parking.address, self.address)
        self.assertEqual(parking.parking_unit, 'P1 U1')
        self.assertEqual(parking.available_start, today)
        self.assertEqual(parking.payment_amount, 100)
        self.assertEqual(parking.payment_frequency, 'MONTHLY')
        self.assertEqual(parking.staff_approved, 'PENDING')

    def test_invalid_address(self):
        with self.assertRaises(ValueError) as context:
            Parking.objects.create(
            lessor=self.lessor_user,
            address='INVALID ADDRESS',
            parking_unit='P1 U1',
            available_start=timezone.now().date())
        self.assertIn('"Parking.address" must be a "Address" instance',
                      str(context.exception))
        
    def test_invalid_start_date(self):
        with self.assertRaises(ValidationError) as context:
            Parking.objects.create(
            lessor=self.lessor_user,
            address=self.address,
            parking_unit='P1 U1',
            available_start=timezone.now().date() - timedelta(days=10))
        self.assertIn('Start date must be today or in the future.',
            str(context.exception))

    def test_invalid_end_date(self):
        with self.assertRaises(ValidationError) as context:
            Parking.objects.create(
            lessor=self.lessor_user,
            address=self.address,
            parking_unit='P1 U1',
            available_start=timezone.now().date(),
            available_end=timezone.now().date() - timedelta(days=10))
        self.assertIn('End date must be later than start date.',
            str(context.exception))

class LeaseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.address = Address.objects.create(
            street = 'street1',
            street_no = 1, 
            city = 'city1',
            state = 'state1',
            postal_code = 'postal_code1',
            country = 'country1',
        )

        cls.tenant_user1 = User.objects.create(
            username='Tenant1User', 
            password='TU1@123!'
        )
        cls.tenant_user2 = User.objects.create(
            username='Tenant2User', 
            password='TU2@123!'
        )

        cls.lessor_user1 = User.objects.create(
            username='Lessor1User', 
            password='LU1@123!'
        )
        cls.lessor_user2 = User.objects.create(
            username='Lessor2User', 
            password='LU2@123!'
        )

        cls.vehicle = Vehicle.objects.create(
            owner=cls.tenant_user1, 
            make='make1',
            model='model1',
            colour='colour1',
            license_plate='license1')

        cls.future_date = timezone.now().date() + timedelta(days=15)
        cls.parking = Parking.objects.create(
            lessor=cls.lessor_user1,
            address=cls.address,
            parking_unit='P1 U1',
            available_start=cls.future_date,
            available_end=cls.future_date + timedelta(days=30),
            payment_amount=100,
            payment_frequency='MONTHLY')

    def test_lease_creation(self):
        lease = Lease.objects.create(
            parking=self.parking,
            vehicle=self.vehicle,
            lessor=self.lessor_user1,
            lessor_approved='APPROVED',
            tenant=self.tenant_user1,
            tenant_approved='APPROVED',
            start_date = self.future_date + timedelta(days=5),
            end_date = self.future_date + timedelta(days=15),
            staff_approved='APPROVED',
            payment_frequency='ANNUALLY',
            payment_type='CREDIT',
            payment_details='payment details 1',
            payment_amount=100
        )

        self.assertEqual(lease.parking, self.parking)
        self.assertEqual(lease.vehicle, self.vehicle)
        self.assertEqual(lease.lessor, self.lessor_user1)
        self.assertEqual(lease.lessor_approved, 'APPROVED')
        self.assertEqual(lease.tenant, self.tenant_user1)
        self.assertEqual(lease.tenant_approved, 'APPROVED')
        self.assertEqual(lease.start_date, self.future_date + timedelta(days=5))
        self.assertEqual(lease.end_date, self.future_date + timedelta(days=15))
        self.assertEqual(lease.staff_approved, 'APPROVED'),
        self.assertEqual(lease.payment_frequency, 'ANNUALLY')
        self.assertEqual(lease.payment_type, 'CREDIT')
        self.assertEqual(lease.payment_details, 'payment details 1')   
        self.assertEqual(lease.payment_amount, 100)


    def test_invalid_start(self):
        with self.assertRaises(ValidationError) as context:
            Lease.objects.create(
            parking=self.parking,
            vehicle=self.vehicle,
            lessor=self.lessor_user1,
            tenant=self.tenant_user1,
            start_date = self.future_date - timedelta(days=5),
            end_date = self.future_date + timedelta(days=15),
            payment_frequency='ANNUALLY',
            payment_type='CREDIT',
            payment_details='payment details 1',
            payment_amount=100
        )
        self.assertIn('Lease start date shouldn\'t be earlier than available start date.',
                        str(context.exception))

    def test_invalid_end(self):
        with self.assertRaises(ValidationError) as context:
            Lease.objects.create(
            parking=self.parking,
            vehicle=self.vehicle,
            lessor=self.lessor_user1,
            tenant=self.tenant_user1,
            start_date = self.future_date + timedelta(days=5),
            end_date = self.future_date + timedelta(days=60),
            payment_frequency='ANNUALLY',
            payment_type='CREDIT',
            payment_details='payment details 1',
            payment_amount=100
        )
        self.assertIn('Lease start date shouldn\'t be later than available end date.',
                        str(context.exception))

    def test_invalid_payment_frequency(self):
        with self.assertRaises(ValidationError) as context:
            Lease.objects.create(
            parking=self.parking,
            vehicle=self.vehicle,
            lessor=self.lessor_user1,
            tenant=self.tenant_user1,
            start_date=self.future_date + timedelta(days=5),
            end_date=self.future_date + timedelta(days=15),
            payment_frequency='BAD CHOICE',
            payment_type='CREDIT',
            payment_details='payment details 1',
            payment_amount=100
        )
        self.assertIn("'BAD CHOICE' is not a valid choice.",
                      str(context.exception))

    def test_invalid_payment_type(self):
        with self.assertRaises(ValidationError) as context:
            Lease.objects.create(
            parking=self.parking,
            vehicle=self.vehicle,
            lessor=self.lessor_user1,
            tenant=self.tenant_user1,
            start_date=self.future_date + timedelta(days=5),
            end_date=self.future_date + timedelta(days=15),
            payment_frequency='ANNUALLY',
            payment_type='BAD CHOICE',
            payment_details='payment details 1',
            payment_amount=100
        )
        self.assertIn("'BAD CHOICE' is not a valid choice.",
                      str(context.exception))
        
    def test_invalid_tenant(self):
        with self.assertRaises(ValidationError) as context:
            Lease.objects.create(
            parking=self.parking,
            vehicle=self.vehicle,
            lessor=self.lessor_user1,
            tenant=self.tenant_user2,
            start_date=self.future_date + timedelta(days=5),
            end_date=self.future_date + timedelta(days=15),
            payment_frequency='ANNUALLY',
            payment_type='CREDIT',
            payment_details='payment details 1',
            payment_amount=100
        )
        self.assertIn('The vehicle owner must be the tenant on the lease.',
                      str(context.exception))
        
    def test_invalid_lessor(self):
        with self.assertRaises(ValidationError) as context:
            Lease.objects.create(
            parking=self.parking,
            vehicle=self.vehicle,
            lessor=self.lessor_user2,
            tenant=self.tenant_user1,
            start_date=self.future_date + timedelta(days=5),
            end_date=self.future_date + timedelta(days=15),
            payment_frequency='ANNUALLY',
            payment_type='CREDIT',
            payment_details='payment details 1',
            payment_amount=100

        )
        self.assertIn('The parking spot must belong to the lessor on the lease.',
                      str(context.exception))






        

