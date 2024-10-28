from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.address_views import AddressViewSet
from .views.parking_views import ParkingViewSet
from .views.vehicle_views import VehicleViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'address', AddressViewSet, basename='address')
router.register(r'parking', ParkingViewSet, basename='parking')
router.register(r'vehicle', VehicleViewSet, basename='vehicle')

urlpatterns = [
    path('', include(router.urls)),
    path('address/<int:pk>/add_user/', AddressViewSet.as_view({'post': 'add_staff_user'}), name='add-staff-user'),
    path('address/<int:pk>/remove_user/', AddressViewSet.as_view({'delete': 'remove_staff_user'}), name='remove-staff-user'),
]