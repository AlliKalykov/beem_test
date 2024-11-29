from rest_framework import serializers

from abc_back.products.models import Brand, Category, Color, Product, Size, SubProduct


class CategoryShortSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для категории."""

    class Meta:
        model = Category
        fields = ("id", "name", "is_featured", "parent")


class RecursiveCategorySerializer(serializers.Serializer):
    """Рекурсивный сериализатор для категорий."""

    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class ParentCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий с иерархией от нижнего уровня до корня."""

    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "is_featured", "parent")

    def get_parent(self, obj):
        if not obj.parent:
            return None  # Если нет родительской категории, возвращаем None
        return ParentCategorySerializer(obj.parent, context=self.context).data


class CategoryTreeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения всех категорий в виде дерева."""

    children = RecursiveCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "is_featured", "children")


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


class ProductShortSerializer(serializers.ModelSerializer):
    sub_products = SubProductShortSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "poster", "brand", "sub_products",
        )


class ProductSerializer(ProductShortSerializer):
    """Сериализатор для товаров с категорией и иерархией от главной категории до текущей."""

    category = ParentCategorySerializer(many=True, read_only=True)

    class Meta(ProductShortSerializer.Meta):
        fields = ProductShortSerializer.Meta.fields + (
            "is_novelty", "is_bestseller", "is_back_in_stock", "is_recommendation", "description", "use", "ingredient",
            "additional", "category",
        )
