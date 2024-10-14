from http import HTTPStatus

from rest_framework.exceptions import APIException


class BadRequest(APIException):
    status_code = HTTPStatus.BAD_REQUEST
    default_detail = "Bad request."
    default_code = "bad_request"
