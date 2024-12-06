from django.db.models import QuerySet

from abc_back.exceptions import NotFoundError
from abc_back.types import Id
from abc_back.users.models import User


class UserRepository:
    """Репозиторий для работы с данными пользователей."""

    def get_active(self) -> QuerySet[User]:
        """Получение активных пользователей."""
        return User.objects.filter(is_active=True, tb_id__isnull=False)

    def get_by_pk(self, user_pk: Id, /, *, active: bool = False) -> User:
        """Получение пользователя по ID."""
        base_manager = User.active if active else User.objects
        try:
            user = base_manager.get(pk=user_pk)
        except User.DoesNotExist:
            raise NotFoundError
        return user

    def get_by_pks(self, user_pks: list[Id], /, *, active: bool = False) -> QuerySet[User]:
        """Получение пользователей по списку ID."""
        base_manager = User.active if active else User.objects
        return base_manager.filter(pk__in=user_pks)

    def get_by_email(self, email: str, /, *, active: bool = False) -> User:
        """Получение пользователя по почте."""
        base_manager = User.active if active else User.objects
        try:
            user = base_manager.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise NotFoundError
        return user

    def create_user(
        self, email: str, password: str, middle_name: str | None, first_name: str = "", last_name: str = "",
    ) -> User | None:
        """Создание пользователя."""
        if User.objects.filter(email=email).exists():
            return
        return User.objects.create_user(
            email=email, password=password, first_name=first_name, last_name=last_name, middle_name=middle_name
        )
