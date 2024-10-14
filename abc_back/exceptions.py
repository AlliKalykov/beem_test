from __future__ import annotations

import enum
import logging
from http import HTTPStatus
from typing import TYPE_CHECKING

from rest_framework.exceptions import APIException

if TYPE_CHECKING:
    import requests


log = logging.getLogger(__name__)


class ErrorMessage(str, enum.Enum):
    """Описание ошибки."""

    SERVER_UNHANDLED = "Server error"


class ErrorCode(str, enum.Enum):
    """Код ошибки."""

    ERROR = "error"
    SERVER = "server"
    CLIENT = "client"


class HTTPError(Exception):
    _message: str
    _messages: list[str]
    _error_dict: dict | None

    def __init__(self, response: requests.Response) -> None:
        self.response = response

    @property
    def status_code(self) -> int:
        return self.response.status_code

    @property
    def message(self) -> str | None:
        try:
            return self._message
        except AttributeError:
            pass
        try:
            self._message = self.messages[0]
        except IndexError:
            self._message = None
        return self._message

    @property
    def messages(self) -> list[str]:
        try:
            return self._messages
        except AttributeError:
            pass
        messages = None
        if self.error_dict:
            if not (messages := self.error_dict.get("errors")):
                if message := self.error_dict.get("error_description") or self.error_dict.get("error"):
                    messages = [message]
        elif self.response.text:
            messages = [self.response.text]
        self._messages = messages or []
        return self._messages

    @property
    def error_dict(self) -> dict | None:
        try:
            return self._error_dict
        except AttributeError:
            pass
        try:
            response_json = self.response.json()
        except ValueError:
            self._error_dict = None
            return None
        if not isinstance(response_json, dict):
            log.warning(f"unexpected error body: {response_json!r}")
            self._error_dict = None
        else:
            self._error_dict = response_json
        return self._error_dict

    def __str__(self) -> str:
        return f"{self.status_code}: {self.message}"


class ServerError(HTTPError):
    pass


class ClientError(HTTPError):
    exc_status_code = HTTPStatus.BAD_REQUEST


class InvalidAccessTokenError(ClientError):
    exc_status_code = HTTPStatus.UNAUTHORIZED


class AccessTokenExpiredError(ClientError):
    exc_status_code = HTTPStatus.UNAUTHORIZED


class MaxAttemptsError(Exception):
    exc_status_code = HTTPStatus.BAD_REQUEST


class NotFoundError(APIException):
    """Ресурс не найден."""

    status_code = HTTPStatus.NOT_FOUND
    default_code = "resource_not_found"
    default_detail = "Resource not found."


class BadRequestError(APIException):
    """Неверный запрос."""

    status_code = HTTPStatus.BAD_REQUEST
    default_code = "bad_request"
    default_detail = "Bad request."


class ForbiddenError(APIException):
    """Запрос не обработан."""

    status_code = HTTPStatus.FORBIDDEN
    default_code = "forbidden"
    default_detail = "Forbidden."


class UnprocessableEntityError(APIException):
    """Запрос не обработан."""

    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    default_code = "unprocessable_entity"
    default_detail = "Unprocessable entity."
