import enum
from typing import NamedTuple, Optional, Type

from rest_framework.exceptions import APIException, NotAuthenticated, NotFound, PermissionDenied, ValidationError

from abc_back.api.exceptions import BadRequest


class _ErrorCode(NamedTuple):
    exception_class: Type[APIException]
    # поле detail ответа с ошибкой
    message: str
    # опциональное описание для документации, не доступно через API
    description: Optional[str] = None


class ErrorCode(_ErrorCode, enum.Enum):
    # 400
    BAD_REQUEST = BadRequest, "Неверный запрос."
    EMAIL_ALREADY_TAKEN = BadRequest, "Email уже зарегистрирован."
    VALIDATION_ERROR = ValidationError, "Ошибка валидации."
    INVALID_TOKEN = BadRequest, "Неправильный токен."
    # 401
    NOT_AUTHENTICATED = NotAuthenticated, "Требуется аутентификация."
    # 403
    AUTHENTICATION_FAILED = PermissionDenied, "Ошибка аутентификации."
    TOO_MANY_ATTEMPTS = PermissionDenied, "Исчерпан лимит попыток."
    AUTHENTICATION_REQUIRED = PermissionDenied, "Требуется аутентификация."
    TOKEN_EXPIRED = PermissionDenied, "Токен истек."
    # 404
    NOT_FOUND = NotFound, "Объект не найден."
    TOKEN_NOT_FOUND = NotFound, "Токен не найден."

    @property
    def code(self) -> str:
        return self.name

    @property
    def message(self) -> str:
        return self.value.message

    @property
    def exception_class(self) -> Type[APIException]:
        return self.value.exception_class

    @property
    def status_code(self) -> int:
        return self.value.exception_class.status_code

    @property
    def description(self) -> Optional[str]:
        return self.value.description

    def __str__(self) -> str:
        return self.code

    def __repr__(self) -> str:
        return f"<ErrorCode.{self.code}: {self.message}>"

    def as_exception(self, message: Optional[str] = None) -> APIException:
        return self.exception_class(message or self.message, self.code)
