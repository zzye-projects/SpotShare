from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.address_views import AddressViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'address', AddressViewSet, basename='address')

urlpatterns = [
    path('', include(router.urls)),
    path('address/<int:pk>/add_user/', AddressViewSet.as_view({'post': 'add_user'}), name='add-user'),
    path('address/<int:pk>/remove_user/', AddressViewSet.as_view({'delete': 'remove_user'}), name='remove-user'),
]