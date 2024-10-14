import datetime
import re
from typing import Any, Optional

from rest_framework.serializers import *  # noqa

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator as DjangoEmailValidator
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


class Validator(Serializer):  # noqa
    """Валидатор для проверки пользовательских данных."""

    @classmethod
    def check(cls, data: dict, context: dict[str, Any]) -> bool:
        instance = cls(data=data, context=context)

        return instance.is_valid(raise_exception=True)


class NameValidator(RegexValidator):
    regex = r"^[a-zA-Zа-яА-ЯёЁ]+(-[a-zA-Zа-яА-ЯёЁ]+)*$"
    message = _("Пожалуйста, введите корректные данные.")
    code = "invalid_name"


class PhoneValidator(RegexValidator):
    regex = r"^7\d{10}$"
    message = _("Пожалуйста, введите корректный номер телефона.")
    code = "invalid_phone"


@deconstructible
class MaxFileSizeValidator:
    """Валидация максимального размера файла."""

    default_error_message = "размер файла больше допустимого {0}"
    default_error_code = "invalid"

    def __init__(
        self, max_file_size: int,
        error_message: str = None,
        field_name: Optional[str] = None,
        err_code: str = None,
    ):
        self.max_size = max_file_size
        assert self.max_size, "It can't be null"
        assert isinstance(self.max_size, int), "It should be int"
        self.file_size_prefix = self.get_file_size_prefix()
        self.error_message = error_message or self.default_error_message.format(self.file_size_prefix)
        self.field_name = field_name
        self.error_code = err_code or self.default_error_code

    def __call__(self, value):
        if value.size > self.max_size:
            self._raise_error()

    def get_file_size_prefix(self) -> str:
        if self.max_size < 1024:
            return "{}B".format(self.max_size)
        elif self.max_size < 1024 * 1024:
            return "{}KB".format(self.max_size // 1024)
        elif self.max_size < 1073741824:
            return "{}MB".format(self.max_size // 1048576)
        return "{}GB".format(self.max_size // 1073741824)

    def _raise_error(self):
        if self.field_name:
            raise ValidationError({self.field_name: self.error_message}, code=self.error_code)
        raise ValidationError(self.error_message, code=self.error_code)


def validate_email(value: str) -> None:
    """Валидация email. Доступны только латинские буквы, цифры и символы: ._-+, которые не идут подряд."""
    message = _("Пожалуйста, введите корректный email.")
    DjangoEmailValidator(message)(value)
    symbols = r"^(?!.*[+\-_.]{2})[A-Za-z0-9\+\-\_\.]+$"
    if not re.match(symbols, value.split("@")[0]):
        raise ValidationError(
            message,
            code="invalid",
        )


def validate_date_of_birth(value):
    if not datetime.date(1900, 1, 1) <= value <= datetime.date.today():
        raise ValidationError(
            _("Пожалуйста, введите корректную дату рождения."),
            code="invalid",
        )
