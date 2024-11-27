from rest_framework import serializers

from abc_back.products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent", "is_featured")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "poster", "category", "brand", "is_novelty", "is_bestseller", "is_back_in_stock",
            "is_recommendation", "description", "use", "ingredient", "additional",
        )
