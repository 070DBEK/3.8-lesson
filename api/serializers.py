from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, ProductImage, Customer, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.StringRelatedField(source='parent', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'parent_name', 'image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='category', read_only=True)
    category_by_name = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
        source='category'
    )
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'discount_price',
            'category', 'category_name', 'category_by_name', 'images',
            'stock', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        existing_images = {image.id: image for image in instance.images.all()}
        for image_data in images_data:
            image_id = image_data.get('id', None)
            if image_id and image_id in existing_images:
                image = existing_images.pop(image_id)
                for attr, value in image_data.items():
                    setattr(image, attr, value)
                image.save()
            else:
                ProductImage.objects.create(product=instance, **image_data)
        for image in existing_images.values():
            image.delete()
        return instance


class CategoryDetailSerializer(CategorySerializer):
    products_info = serializers.SerializerMethodField()

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['products_info']

    def get_products_info(self, obj):
        products = obj.products.all()
        return {
            'count': products.count(),
            'products': [
                {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price
                }
                for product in products[:5]
            ]
        }


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.StringRelatedField(source='product', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'created_at']
        read_only_fields = ['id', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    customer_username = serializers.StringRelatedField(source='customer.user.username', read_only=True)
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_username', 'status', 'total_price',
            'shipping_address', 'payment_method', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        existing_items = {item.id: item for item in instance.items.all()}
        for item_data in items_data:
            item_id = item_data.get('id', None)
            if item_id and item_id in existing_items:
                # Update existing item
                item = existing_items.pop(item_id)
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                item.save()
            else:
                OrderItem.objects.create(order=instance, **item_data)
        for item in existing_items.values():
            item.delete()
        return instance


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'username', 'email', 'phone', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
