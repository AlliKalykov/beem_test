from __future__ import annotations

from rest_framework import mixins, viewsets

from abc_back.api.views import MultiSerializerViewSetMixin
from abc_back.api.pagination import DefaultPageNumberPagination

from abc_back.blogs.models import Category, Post

from .serializers import CategoryShortSerializer, PostDetailSerializer, PostSerializer


class CategoryViewSet(
    MultiSerializerViewSetMixin, viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
):
    queryset = Category.objects.all()
    permission_classes = []
    pagination_class = DefaultPageNumberPagination
    lookup_field = "slug"

    serializer_classes = {
        "list": CategoryShortSerializer,
        "retrieve": CategoryShortSerializer,
    }


class PostViewSet(
    MultiSerializerViewSetMixin, viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
):
    queryset = Post.objects.all()
    permission_classes = []
    pagination_class = DefaultPageNumberPagination
    lookup_field = "slug"

    serializer_classes = {
        "list": PostSerializer,
        "retrieve": PostDetailSerializer,
    }
