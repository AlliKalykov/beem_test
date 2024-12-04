from rest_framework import serializers

from abc_back.api.v1.products.serializers import ProductShortSerializer
from abc_back.blogs.models import Category, Post


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class PostShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "slug", "poster", "is_active")


class PostSerializer(PostShortSerializer):
    categories = CategoryShortSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "slug", "poster", "is_active", "text", "categories")


class PostDetailSerializer(PostSerializer):
    authors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    related_post = PostShortSerializer(many=True, read_only=True)
    related_product = ProductShortSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id", "title", "slug", "poster", "is_active", "text", "categories",
            "authors", "related_post", "related_product",
        )
