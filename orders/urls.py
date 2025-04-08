from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CustomerViewSet, OrderViewSet, OrderItemViewSet


router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')


urlpatterns = [
    path('', include(router.urls)),
]
