from __future__ import annotations

import logging
import textwrap
from collections import defaultdict
from typing import TYPE_CHECKING, Type

# from drf_spectacular.authentication import TokenScheme
from drf_spectacular.utils import OpenApiResponse, PolymorphicProxySerializer
from drf_spectacular.utils import extend_schema as original_extend_schema
from rest_framework import serializers

#
from abc_back.api.constants import ErrorCode


log = logging.getLogger(__name__)


if TYPE_CHECKING:
    from collections.abc import Sequence

    from rest_framework.serializers import Serializer

    _ErrorCodePair = tuple[ErrorCode, str]
    _ErrorCode = ErrorCode | _ErrorCodePair
    _ErrorCodeList = Sequence[_ErrorCode]


def _dedent_text(text: str) -> str:
    return textwrap.dedent(text).strip()


def _concat_text(*parts: str) -> str:
    return "\n\n".join(parts)


def _format_error_code_list_item(error_code: _ErrorCode) -> str:
    extra_description: str | None = None
    if not isinstance(error_code, ErrorCode):
        error_code, extra_description = error_code
    parts: list[str] = [f"* `{error_code.code}` _{error_code.message}_"]
    if description := error_code.description:
        parts.append(description)
    if extra_description:
        parts.append(extra_description)
    return " ".join(parts)


def _format_error_code_list(error_codes: _ErrorCodeList) -> str:
    return "\n".join(map(_format_error_code_list_item, error_codes))


class RegularErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField(allow_null=True)


class ValidationErrorResponseSerializer(serializers.Serializer):
    detail = serializers.DictField(child=serializers.ListField(child=serializers.CharField()))
    code = serializers.ChoiceField(choices=[ErrorCode.VALIDATION_ERROR.code])


bad_request_polymorphic_serializer = PolymorphicProxySerializer(
    component_name="BadRequestErrorResponse",
    serializers=[RegularErrorResponseSerializer, ValidationErrorResponseSerializer],
    resource_type_field_name=None,
)


def regular_error_response(description: str = "", error_codes: _ErrorCodeList | None = None) -> OpenApiResponse:
    """Ответ для "обычных" ошибок."""
    description = _dedent_text(description)
    if error_codes:
        description = _concat_text(description, _format_error_code_list(error_codes))
    return OpenApiResponse(RegularErrorResponseSerializer, description)


def validation_error_response(description: str = "Ошибка валидации.") -> OpenApiResponse:
    """Ответ для ошибок валидации."""
    return OpenApiResponse(ValidationErrorResponseSerializer, _dedent_text(description))


def bad_request_error_response(description: str = "", error_codes: _ErrorCodeList | None = None) -> OpenApiResponse:
    """Ответ для ошибок 400. Особый случай, если может быть как ошибка валидации, так и "обычная" ошибка."""
    description = _dedent_text(description)
    if error_codes:
        if ErrorCode.VALIDATION_ERROR not in error_codes:
            error_codes = [ErrorCode.VALIDATION_ERROR, *error_codes]
    else:
        error_codes = [ErrorCode.VALIDATION_ERROR]
    description = _concat_text(description, _format_error_code_list(error_codes))
    return OpenApiResponse(bad_request_polymorphic_serializer, description)


def unauthorized_error_response(description: str = "", error_codes: _ErrorCodeList | None = None) -> OpenApiResponse:
    """Ответ для ошибок 401, генерируемых DRF"ом (третий пункт).

    https://www.django-rest-framework.org/api-guide/permissions/#how-permissions-are-determined
    """
    if not error_codes:
        error_codes = (ErrorCode.AUTHENTICATION_REQUIRED, ErrorCode.AUTHENTICATION_FAILED)
    return regular_error_response(description, error_codes)


def extend_schema(
    responses: dict[int | ErrorCode, OpenApiResponse | Serializer | Type[Serializer] | str | None], **kwargs,
):
    processed_responses: dict[int, OpenApiResponse | Serializer | Type[Serializer]] = {}
    response_error_codes: defaultdict[int, list[_ErrorCode]] = defaultdict(list)

    for code, response in responses.items():
        if isinstance(code, int):
            if response is None:
                response = OpenApiResponse(None)
            elif isinstance(response, str):
                response = OpenApiResponse(None, response)
            processed_responses[int(code)] = response
        else:
            if response is None:
                _error_code = code
            elif isinstance(response, str):
                _error_code = (code, response)
            else:
                message = f"{code!r}: unexpected response {response!r}"
                log.error(message)
                raise AssertionError(message)
            response_error_codes[code.status_code].append(_error_code)

    for status_code, error_codes in response_error_codes.items():
        if status_code in processed_responses:
            log.error("Status Code not in processed responses")
        assert status_code not in processed_responses
        if ErrorCode.VALIDATION_ERROR in error_codes:
            if len(error_codes) == 1:
                response = validation_error_response()
            else:
                response = bad_request_error_response(error_codes=error_codes)
        else:
            response = regular_error_response(error_codes=error_codes)
        processed_responses[status_code] = response

    return original_extend_schema(responses=processed_responses, **kwargs)
