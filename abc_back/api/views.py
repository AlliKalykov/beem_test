from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type

if TYPE_CHECKING:
    from rest_framework.serializers import Serializer
    from rest_framework.throttling import BaseThrottle

    from django.db.models.query import QuerySet


class MultiSerializerViewSetMixin:
    """Миксин для выбора нужного сериалайзера из `serializer_classes`."""

    serializer_classes: Optional[dict[str, Type[Serializer]]] = None

    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except KeyError:
            return super().get_serializer_class()


class MultiPermissionViewSetMixin:
    """Миксин для выбора нужных прав доступа из `permission_action_map`."""

    permission_action_map: Optional[dict[str, Type[list]]] = None

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_action_map[self.action]]
        except KeyError:
            return super().get_permissions()


class MultiQuerysetViewSetMixin:
    """Миксин для выбора нужного queryset'а из `queryset_action_map`."""

    queryset_action_map: Optional[dict[str, Type[QuerySet]]]

    def get_queryset(self):
        try:
            return self.queryset_action_map[self.action]
        except KeyError:
            return super().get_queryset()


class MultiThrottllesViewSetMixin:
    """Миксин для выбора нужного throttle'а из `throttle_classes`."""

    throttle_classes: Optional[dict[str, Type[list[BaseThrottle]]]] = None

    def get_throttles(self) -> list[BaseThrottle]:
        return [throttle() for throttle in self.throttle_classes.get(self.action, [])]

    def check_throttles(self, request) -> None:
        not_allowed_throttles = []
        for throttle in self.get_throttles():
            if not throttle.allow_request(request, self):
                not_allowed_throttles.append(throttle)
        max_duration_throttle = max(not_allowed_throttles,
                                    key=lambda throttle: throttle.wait(),
                                    default=None)
        if max_duration_throttle is not None:
            self.throttled(request, max_duration_throttle)

    def throttled(self, request, throttle) -> None:
        raise throttle.exception_class(throttle.wait())
