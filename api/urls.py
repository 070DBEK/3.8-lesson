from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, CustomerViewSet, OrderViewSet,
    DashboardStatsView, TopProductsView, TopCustomersView, RevenueStatsView
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('dashboard/top-products/', TopProductsView.as_view(), name='top-products'),
    path('dashboard/top-customers/', TopCustomersView.as_view(), name='top-customers'),
    path('dashboard/revenue/', RevenueStatsView.as_view(), name='revenue-stats'),
]
