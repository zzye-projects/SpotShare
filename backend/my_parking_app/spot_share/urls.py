from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.address_views import AddressViewSet
from .views.parking_views import ParkingViewSet
from .views.vehicle_views import VehicleViewSet
from .views.lease_views import LeaseViewSet
from .views.staff_user_views import StaffUserView, SingleStaffUserView

router = DefaultRouter(trailing_slash=False)
router.register(r'address', AddressViewSet, basename='address')
router.register(r'parking', ParkingViewSet, basename='parking')
router.register(r'vehicle', VehicleViewSet, basename='vehicle')
router.register(r'lease', LeaseViewSet, basename='lease')


urlpatterns = [
    path('', include(router.urls)),
    path('address/<int:pk>/add_user/', AddressViewSet.as_view({'post': 'add_staff_to_address'}), name='add-staff-to-address'),
    path('address/<int:pk>/remove_user/', AddressViewSet.as_view({'delete': 'remove_staff_from_address'}), name='remove-staff-from-address'),
    path('groups/staff/users', StaffUserView.as_view(), name='staff-list'),
    path('groups/staff/users/<int:pk>', SingleStaffUserView.as_view(), name='staff-detail'),
]