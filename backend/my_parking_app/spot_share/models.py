from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
from .globals import PAYMENT_CHOICES, FREQUENCY_CHOICES, APPROVAL_CHOICES

def validate_dates(start_date, end_date):
    if start_date < timezone.now().date():
        raise ValidationError('Start date must be today or in the future.')

    if end_date and start_date >= end_date:
        raise ValidationError('End date must be later than start date.')
            
class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    colour = models.CharField(max_length=30)
    license_plate = models.CharField(
        max_length=15, 
        unique=True,
        db_index=True)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.license_plate

class Address(models.Model):
    street = models.CharField(max_length=255)
    street_no = models.SmallIntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, unique=True)
    country = models.CharField(max_length=100)
    staff_users = models.ManyToManyField(User, related_name='addresses')

    def add_staff_user(self, user):        
        if not user.groups.filter(name='Staff').exists():
            raise ValidationError(f'{user.username} is not Staff user. Only staff can be associated to an address.')
        self.staff_users.add(user)

    def __str__(self):
        return f'{self.street_no} {self.street}, {self.city}, {self.state} {self.postal_code}, {self.country}'

class Parking(models.Model):
    STATUS_CHOICES = [
        ('DRAFT','Draft'),
        ('ACTIVE','Active'),
        ('ARCHIVED', 'Archived')
    ]
    lessor = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    parking_unit = models.CharField(max_length=50)
    available_start = models.DateField(db_index=True)
    available_end = models.DateField(
        db_index=True, 
        null=True,
        blank=True)
    staff_approved = models.CharField(
        max_length=10,
        choices=APPROVAL_CHOICES,
        default='PENDING'
    )
    payment_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    payment_frequency=models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES
    )

    def clean(self):
        super().clean()
        validate_dates(self.available_start, self.available_end)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.address} - {self.parking_unit}'

class Lease(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, db_index=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, db_index=True)
    
    lessor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_index=True,
        related_name='leases_as_lessor')
    lessor_approved = models.CharField(
        max_length=10,
        choices=APPROVAL_CHOICES,
        default='PENDING'
    )

    tenant = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_index=True,
        related_name='leases_as_tenant') 
    tenant_approved = models.CharField(
        max_length=10,
        choices=APPROVAL_CHOICES,
        default='PENDING'
    )

    start_date = models.DateField(db_index=True)
    end_date = models.DateField(
        db_index=True, 
        null=True, 
        blank=True)
    staff_approved = models.CharField(
        max_length=10,
        choices=APPROVAL_CHOICES,
        default='PENDING'
    )
    payment_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    payment_frequency=models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES
    )
    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES
    )
    # Add additional payment integrations/details in the future
    payment_details = models.CharField(max_length=255)
    
    def clean(self):
        super().clean()
        validate_dates(self.start_date, self.end_date)

        if self.start_date < self.parking.available_start:
            raise ValidationError('Lease start date shouldn\'t be earlier than available start date.')
        
        if (not self.end_date and self.parking.available_end) or \
        (self.end_date and self.parking.available_end and self.end_date > self.parking.available_end):
            raise ValidationError('Lease start date shouldn\'t be later than available end date.')
        
        if (self.parking.lessor != self.lessor):
            raise ValidationError('The parking spot must belong to the lessor on the lease.')
        
        if (self.vehicle.owner != self.tenant):
            raise ValidationError('The vehicle owner must be the tenant on the lease.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.parking}: {self.vehicle}'
    


