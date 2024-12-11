from __future__ import annotations

from rest_framework import serializers

from abc_back.api.v1.products.serializers import SubProductShortSerializer
from abc_back.cart.models import CartItem


class CartItemShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "sub_product", "quantity"]


class CartItemSerializer(CartItemShortSerializer):
    sub_product = SubProductShortSerializer(read_only=True)

    class Meta(CartItemShortSerializer.Meta):
        fields = CartItemShortSerializer.Meta.fields
