from django.contrib import admin
from .models import Customer, Order, OrderItem


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'address', 'created_at', 'updated_at')
    search_fields = ('user__username', 'phone')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'created_at')
    list_filter = ('order', 'product')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'shipping_address', 'payment_method', 'created_at', 'updated_at')
    search_fields = ('customer__user__username', 'status')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemAdmin]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
