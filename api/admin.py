from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, Customer, Order, OrderItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'description', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'parent')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_primary')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_price', 'category', 'stock', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductImageInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category')
        }),
        ('Pricing and Inventory', {
            'fields': ('price', 'discount_price', 'stock', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image_preview', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name',)
    readonly_fields = ('created_at', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Image Preview'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'phone', 'address')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'phone', 'address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('product', 'quantity', 'price')
    raw_id_fields = ('product',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'payment_method', 'created_at', 'updated_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('customer__user__username', 'shipping_address')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
    fieldsets = (
        (None, {
            'fields': ('customer', 'status', 'total_price')
        }),
        ('Shipping and Payment', {
            'fields': ('shipping_address', 'payment_method')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('order__id', 'product__name')
    readonly_fields = ('created_at',)
    raw_id_fields = ('order', 'product')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)