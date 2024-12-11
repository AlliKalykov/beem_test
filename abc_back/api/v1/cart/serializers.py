from __future__ import annotations

from rest_framework import serializers

from abc_back.api.v1.products.serializers import SubProductShortSerializer
from abc_back.cart.models import Cart, CartItem


class CartItemShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "sub_product", "quantity"]


class CartItemSerializer(CartItemShortSerializer):
    sub_product = SubProductShortSerializer(read_only=True)
    sell_price = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=10)
    sale_percent = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=10)
    final_price = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=10)
    total_price = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=10)

    class Meta(CartItemShortSerializer.Meta):
        fields = CartItemShortSerializer.Meta.fields + ["sell_price", "sale_percent", "final_price", "total_price"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "session_key", "items"]  # TODO: убрать после разработоки user и session_key
