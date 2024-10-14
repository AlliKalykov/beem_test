from rest_framework import status
from rest_framework.exceptions import Throttled


class CreateOTPExceptionThrottled(Throttled):
    status_code = status.HTTP_423_LOCKED
    default_detail = "Sending OTP blocked."
    default_code = "throttled_create_otp"


class ValidateOTPExceptionThrottled(Throttled):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = "Validate OTP blocked"
    default_code = "throttled_validate_otp"
