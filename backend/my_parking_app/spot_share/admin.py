from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Address)
admin.site.register(Parking)
admin.site.register(Lease)