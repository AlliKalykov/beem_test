from typing import Any

import sentry_sdk
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework.exceptions import APIException, NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import exception_handler

from abc_back.exceptions import ErrorCode


def sentry_exception_handler(exc: APIException, context: dict[str, Any]) -> Response | None:
    """Логирование всех DRF ошибок в Sentry (включая ValidationErrors)."""
    sentry_sdk.capture_exception(exc)

    response = exception_handler(exc, context)

    if response is None:
        return response

    return _process_exception(response, exc, context)


def _process_exception(response: Response, exc: APIException, context: dict[str, Any]) -> Response:
    if isinstance(exc, Http404):
        exc = NotFound()
    elif isinstance(exc, DjangoPermissionDenied):
        exc = PermissionDenied()

    response.status_code = exc.status_code
    if "detail" in response.data:
        response.data = {
            "detail": None,
            "errors": [
                {
                    "message": getattr(exc, "detail", str(exc)),
                    "code": getattr(exc, "default_code", ErrorCode.ERROR.value),
                },
            ],
        }
        return response
    errors = response.data.copy()
    response.data = []
    if isinstance(errors, list):
        for error in errors:
            error_dict = {
                "detail": None,
                "errors": [
                    {
                        "message": getattr(error, "detail", str(error)),
                        "code": getattr(error, "code", ErrorCode.ERROR.value),
                    },
                ],
            }
            response.data.append(error_dict)
        return response
    if not isinstance(errors, dict):
        return response
    for field, exceptions in errors.items():
        error_dict = {
            "detail": field,
            "errors": [],
        }
        for exception in exceptions:
            error_code = getattr(exception, "default_code", exception.code)
            error_dict["errors"].append({"message": exception, "code": error_code})
        response.data.append(error_dict)
    return response
