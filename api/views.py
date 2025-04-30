from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from .models import Category, Product, ProductImage, Customer, Order, OrderItem
from .serializers import (
    CategorySerializer, CategoryDetailSerializer, ProductSerializer,
    ProductImageSerializer, CustomerSerializer, OrderSerializer, OrderItemSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'])
    def images(self, request, pk=None):
        product = self.get_object()
        serializer = ProductImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='images/(?P<image_id>[^/.]+)')
    def delete_image(self, request, pk=None, image_id=None):
        try:
            image = ProductImage.objects.get(id=image_id, product_id=pk)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductImage.DoesNotExist:
            return Response(
                {"detail": "Image not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        status_value = request.data.get('status')

        if status_value not in dict(Order.STATUS_CHOICES):
            return Response(
                {"detail": "Invalid status value"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = status_value
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        customer = self.get_object()
        orders = customer.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class DashboardStatsView(generics.GenericAPIView):
    def get(self, request):
        # Basic stats
        total_products = Product.objects.count()
        total_orders = Order.objects.count()
        total_customers = Customer.objects.count()
        total_revenue = OrderItem.objects.aggregate(
            total=Sum('price')
        )['total'] or 0

        # Top products
        top_products = Product.objects.annotate(
            total_sold=Sum('orderitem__quantity')
        ).filter(total_sold__gt=0).order_by('-total_sold')[:3]

        top_products_data = [
            {
                'id': product.id,
                'name': product.name,
                'total_sold': product.total_sold,
                'revenue': str(product.price * product.total_sold)
            }
            for product in top_products
        ]

        # Recent orders
        recent_orders = Order.objects.all().order_by('-created_at')[:5]
        recent_orders_serializer = OrderSerializer(recent_orders, many=True)

        return Response({
            'total_products': total_products,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'total_revenue': str(total_revenue),
            'top_products': top_products_data,
            'recent_orders': recent_orders_serializer.data
        })


class TopProductsView(generics.GenericAPIView):
    def get(self, request):
        top_products = Product.objects.annotate(
            total_sold=Sum('orderitem__quantity')
        ).filter(total_sold__gt=0).order_by('-total_sold')[:10]

        top_products_data = [
            {
                'id': product.id,
                'name': product.name,
                'total_sold': product.total_sold,
                'revenue': str(product.price * product.total_sold)
            }
            for product in top_products
        ]

        return Response(top_products_data)


class TopCustomersView(generics.GenericAPIView):
    def get(self, request):
        top_customers = Customer.objects.annotate(
            order_count=Count('orders'),
            total_spent=Sum('orders__total_price')
        ).filter(order_count__gt=0).order_by('-total_spent')[:10]

        top_customers_data = [
            {
                'id': customer.id,
                'username': customer.user.username,
                'order_count': customer.order_count,
                'total_spent': str(customer.total_spent)
            }
            for customer in top_customers
        ]

        return Response(top_customers_data)


class RevenueStatsView(generics.GenericAPIView):
    def get(self, request):
        today = timezone.now().date()

        # Daily revenue (last 7 days)
        daily_revenue = []
        for i in range(7):
            day = today - timedelta(days=i)
            day_revenue = Order.objects.filter(
                created_at__date=day
            ).aggregate(total=Sum('total_price'))['total'] or 0

            daily_revenue.append({
                'date': day.strftime('%Y-%m-%d'),
                'revenue': str(day_revenue)
            })

        # Weekly revenue (last 4 weeks)
        weekly_revenue = []
        for i in range(4):
            week_start = today - timedelta(days=today.weekday() + 7 * i)
            week_end = week_start + timedelta(days=6)

            week_revenue = Order.objects.filter(
                created_at__date__gte=week_start,
                created_at__date__lte=week_end
            ).aggregate(total=Sum('total_price'))['total'] or 0

            weekly_revenue.append({
                'week': f"{week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}",
                'revenue': str(week_revenue)
            })

        # Monthly revenue (last 6 months)
        monthly_revenue = []
        for i in range(6):
            month = today.month - i
            year = today.year

            if month <= 0:
                month += 12
                year -= 1

            month_revenue = Order.objects.filter(
                created_at__year=year,
                created_at__month=month
            ).aggregate(total=Sum('total_price'))['total'] or 0

            monthly_revenue.append({
                'month': f"{year}-{month:02d}",
                'revenue': str(month_revenue)
            })

        return Response({
            'daily': daily_revenue,
            'weekly': weekly_revenue,
            'monthly': monthly_revenue
        })
