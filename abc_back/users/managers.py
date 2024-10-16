from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from django.db import models


if TYPE_CHECKING:
    from abc_back.users.repositories import UserRepository


class ActiveUserManager(models.Manager):
    """Менеджер модели для работы с активными пользователями."""

    @inject
    def get_queryset(self, user_repository: UserRepository = Provide["user_package.user_repository"]):
        return user_repository.get_active()
