from rest_framework import serializers
from .models import Category, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'discount_price', 'category',
                  'stock', 'is_active', 'created_at', 'updated_at', 'images']


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'discount_price', 'category',
                  'stock', 'is_active']


