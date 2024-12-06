from __future__ import annotations


from rest_framework import serializers

from abc_back.api.v1.products.serializers import ProductShortSerializer
from abc_back.api.v1.users.serializers import ProfileShortSerializer
from abc_back.favorites.models import FavoriteProduct


class FavoriteProductShortSerializer(serializers.ModelSerializer):
    user = ProfileShortSerializer(read_only=True)

    class Meta:
        model = FavoriteProduct
        fields = [
            "id", "user", "product",
        ]

    def validate(self, attrs):
        if FavoriteProduct.objects.filter(user=self.context["request"].user, product=attrs["product"]).exists():
            raise serializers.ValidationError("Товар уже добавлен в избранное")
        return attrs


class FavoriteProductSerializer(FavoriteProductShortSerializer):
    product = ProductShortSerializer(read_only=True)

    class Meta(FavoriteProductShortSerializer.Meta):
        fields = FavoriteProductShortSerializer.Meta.fields
