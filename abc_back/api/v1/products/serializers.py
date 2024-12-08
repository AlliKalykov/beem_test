from __future__ import annotations

from drf_spectacular.utils import extend_schema_field

from rest_framework import serializers

from abc_back.products.models import Brand, Category, Color, Product, Size, SubProduct


class CategoryShortSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для категории."""

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "is_featured", "parent")


class RecursiveCategorySerializer(serializers.Serializer):
    """Рекурсивный сериализатор для категорий."""

    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class ParentCategorySerializer(CategoryShortSerializer):
    """Сериализатор для категорий с иерархией от нижнего уровня до корня."""

    parent = serializers.SerializerMethodField()

    class Meta(CategoryShortSerializer.Meta):
        model = Category
        fields = CategoryShortSerializer.Meta.fields

    def get_parent(self, obj):
        if not obj.parent:
            return None  # Если нет родительской категории, возвращаем None
        return ParentCategorySerializer(obj.parent, context=self.context).data


class CategoryTreeSerializer(CategoryShortSerializer):
    """Сериализатор для отображения всех категорий в виде дерева."""

    children = RecursiveCategorySerializer(many=True, read_only=True)

    class Meta(CategoryShortSerializer.Meta):
        model = Category
        fields = CategoryShortSerializer.Meta.fields + ("children",)


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ("id", "name", "hex_code")


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ("id", "name", "kind", "value", "is_active")


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name", "slug", "logo", "description")


class SubProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubProduct
        fields = ("id", "slug", "product", "size", "color", "stock", "is_available", "final_price")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "poster", "brand", "category", "is_novelty", "is_bestseller", "is_back_in_stock",
            "is_recommendation", "description", "use", "ingredient", "additional", "is_active",
        )


class ProductUpdateSerializer(ProductSerializer):
    name = serializers.CharField(required=False)
    slug = serializers.CharField(required=False)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, many=True)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields


class ProductShortSerializer(serializers.ModelSerializer):
    sub_products = serializers.SerializerMethodField()
    brand = BrandSerializer(read_only=True)
    is_favorite = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "poster", "brand", "sub_products", "is_favorite",
        )

    @extend_schema_field(SubProductShortSerializer(many=True))
    def get_sub_products(self, obj):
        # Получение фильтров из запроса
        request = self.context.get('request')
        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')

        sub_products = obj.sub_products.filter(is_available=True)
        if price_min:
            sub_products = sub_products.filter(final_price__gte=price_min)
        if price_max:
            sub_products = sub_products.filter(final_price__lte=price_max)

        return SubProductShortSerializer(sub_products, many=True).data


class ProductListSerializer(ProductShortSerializer):
    """Сериализатор для товаров с категорией и иерархией от главной категории до текущей."""

    category = ParentCategorySerializer(many=True, read_only=True)

    class Meta(ProductShortSerializer.Meta):
        fields = ProductShortSerializer.Meta.fields + (
            "is_novelty", "is_bestseller", "is_back_in_stock", "is_recommendation", "description", "use", "ingredient",
            "additional", "category",
        )
