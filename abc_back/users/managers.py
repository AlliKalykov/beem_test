from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models


if TYPE_CHECKING:
    from abc_back.users.repositories import UserRepository


class ActiveUserManager(models.Manager):
    """Менеджер модели для работы с активными пользователями."""

    @inject
    def get_queryset(self, user_repository: UserRepository = Provide["user_package.user_repository"]):
        return user_repository.get_active()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Creates and saves a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        try:
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
        except AttributeError:
            user = self.model(email=email, password=make_password(password), **extra_fields)
            user._password = password
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
