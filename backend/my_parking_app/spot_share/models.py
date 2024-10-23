from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    colour = models.CharField(max_length=30)
    license_plate = models.CharField(
        max_length=15, 
        unique=True,
        db_index=True)
    
    def __str__(self):
        return self.license_plate