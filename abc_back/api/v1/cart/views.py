from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from abc_back.api.pagination import DefaultPageNumberPagination
from abc_back.api.views import MultiSerializerViewSetMixin
from abc_back.cart.models import CartItem
from abc_back.cart.services import CartService
from abc_back.containers import Container

from .serializers import CartItemSerializer, CartItemShortSerializer, CartSerializer


if TYPE_CHECKING:
    from abc_back.cart.repositories import CartRepository


class CartItemViewSet(
    MultiSerializerViewSetMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = CartItem.objects.none()
    serializer_classes = {
        "list": CartItemSerializer,
        "create": CartItemShortSerializer,
        "retrieve": CartItemShortSerializer,
        "update": CartItemSerializer,
    }
    pagination_class = DefaultPageNumberPagination
    authentication_classes = []
    permission_classes = [AllowAny]
    http_method_names = ["get", "post", "put", "delete"]

    @inject
    def get_queryset(
        self, *, cart_repository: CartRepository = Provide[Container.cart_package.cart_repository],
        cart_service: CartService = Provide[Container.cart_package.cart_service],
    ):
        user_id = self.request.user.id if self.request.user.is_authenticated else None
        cart = cart_service.get_or_create_cart(user_id, self.request.session.session_key)
        cart_items = cart_repository.get_cart_items(cart.id)
        return cart_items

    @inject
    def create(self, request: Request, *, cart_service: CartService = Provide[Container.cart_package.cart_service]):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = self.request.user.id if self.request.user.is_authenticated else None
        session_key = self.request.session.session_key
        sub_product_id = serializer.validated_data["sub_product"].id
        quantity = serializer.validated_data["quantity"]
        cart_item = cart_service.add_item(user_id, session_key, sub_product_id, quantity)
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    @inject
    def update(
        self, request: Request, *, cart_service: CartService = Provide[Container.cart_package.cart_service], pk: int,
    ):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = self.request.user.id if self.request.user.is_authenticated else None
        session_key = self.request.session.session_key
        quantity = serializer.validated_data["quantity"]
        cart_item = cart_service.change_item_quantity(user_id, session_key, pk, quantity)
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)

    @inject
    def destroy(
        self, request: Request, *, cart_service: CartService = Provide[Container.cart_package.cart_service], pk: int,
    ):
        user_id = self.request.user.id if self.request.user.is_authenticated else None
        session_key = self.request.session.session_key
        cart_service.remove_item(user_id, session_key, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartViewSet(viewsets.GenericViewSet):
    queryset = CartItem.objects.none()
    serializer_class = CartSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    @inject
    def get_queryset(
        self, *, cart_repository: CartRepository = Provide[Container.cart_package.cart_repository],
        cart_service: CartService = Provide[Container.cart_package.cart_service],
    ):
        user_id = self.request.user.id if self.request.user.is_authenticated else None
        cart = cart_repository.get_cart_with_calculations(user_id, self.request.session.session_key)
        return cart

    @action(detail=False, methods=["GET"])
    def get(self, request: Request):
        cart = self.get_queryset()
        if cart:
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["DELETE"])
    def delete(
        self, request: Request,
        cart_repository: CartRepository = Provide[Container.cart_package.cart_repository],
    ):
        cart = self.get_queryset()
        if cart:
            cart_repository.delete_cart(cart)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
