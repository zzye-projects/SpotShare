from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.address_views import AddressViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'address', AddressViewSet, basename='address')

urlpatterns = [
    path('', include(router.urls)),
    path('address/<int:pk>/add_user/', AddressViewSet.as_view({'post': 'add_user_to_address'}), name='add-user-to-address'),
]