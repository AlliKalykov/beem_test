from __future__ import annotations

from rest_framework import mixins, viewsets

from abc_back.api.views import MultiSerializerViewSetMixin

from .serializers import CategorySerializer, PostSerializer


class CategoryViewSet(MultiSerializerViewSetMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = CategorySerializer.Meta.model.objects.all()
    permission_classes = []

    serializer_classes = {
        "retrieve": CategorySerializer,
    }


class PostViewSet(MultiSerializerViewSetMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = PostSerializer.Meta.model.objects.all()
    permission_classes = []

    serializer_classes = {
        "retrieve": PostSerializer,
    }
