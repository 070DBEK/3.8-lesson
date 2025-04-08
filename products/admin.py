from django.contrib import admin
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'is_active')
    inlines = [ProductImageInline]


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'is_primary', 'created_at')
    list_filter = ('is_primary',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
