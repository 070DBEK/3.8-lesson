from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'image', 'created_at', 'updated_at']

