from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

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
    
    def clean(self):
        super().clean()
        if not self.owner.groups.filter(name='Tenant').exists():
            raise ValidationError('Vehicle owner must be a parking tenant.')
    
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
    users = models.ManyToManyField(User, related_name='addresses')

    def add_user(self, user):        
        if not user.groups.filter(name='Staff').exists():
            raise ValidationError(f'{user.username} is not Staff user. Only staff can be associated to an address.')
        self.users.add(user)

    def __str__(self):
        return f'{self.street_no} {self.street}, {self.city}, {self.state} {self.postal_code}, {self.country}'

class Parking(models.Model):
    lessor = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    parking_unit = models.CharField(max_length=50)
    available_start = models.DateField(db_index=True)
    available_end = models.DateField(
        db_index=True, 
        null=True,
        blank=True)

    def clean(self):
        super().clean()
        
        if not self.lessor.groups.filter(name='Lessor').exists():
            raise ValidationError('Lessor must be a user who belongs to the Lessor group.')
        validate_dates(self.available_start, self.available_end)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.address} - {self.parking_unit}'

class Lease(models.Model):
    STATUS_CHOICES = [
        ('DRAFT','Draft'),
        ('ACTIVE','Active'),
        ('ARCHIVED', 'Archived')
    ]
    FREQUENCY_CHOICES = [
        ('ANNUALLY','Annually'),
        ('MONTHLY', 'Monthly'),
        ('WEEKLY', 'Weekly')
    ]
    PAYMENT_CHOICES = [
        ('CREDIT', 'Credit'),
        ('DEBIT', 'Pre-Authorized Debit')
    ]
    
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, db_index=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, db_index=True)
    
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(
        db_index=True, 
        null=True, 
        blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='DRAFT'
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

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.parking}: {self.vehicle}'
    


