from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.throttling import BaseThrottle

from .exceptions import CreateOTPExceptionThrottled, ValidateOTPExceptionThrottled


class EmailOTPValidationThrottle(BaseThrottle):
    """Дроссель для валидации otp-токена."""

    exception_class: exceptions.Throttled = ValidateOTPExceptionThrottled

    def get_cache_key(self, request, _):
        return f"otpprove:{request.data.get('email')}"

    def wait(self):
        time_left = self.unblock_time - timezone.now()
        return time_left.seconds

    def allow_request(self, request, view):
        if not settings.ENABLE_THROTTLING:
            return True
        cache_key = self.get_cache_key(request, view)
        token = cache.get(cache_key)
        if token is None:
            return True
        self.unblock_time = token.get("unblock_time")
        if self.unblock_time is None:
            return True
        elif self.unblock_time < timezone.now():
            cache.delete(cache_key)
            return True
        return False


class EmailOTPCreateThrottle(BaseThrottle):
    """Дроссель для отправки otp-токена."""

    exception_class: exceptions.Throttled = CreateOTPExceptionThrottled

    def get_cache_key(self, request, _):
        return f"otpcode:{request.data.get('email')}"

    def wait(self):
        time_left = self.delay_expire_time - timezone.now()
        return time_left.seconds

    def allow_request(self, request, view):
        if not settings.ENABLE_THROTTLING:
            return True
        cache_key = self.get_cache_key(request, view)
        otp_data = cache.get(cache_key)
        if otp_data is None:
            return True
        self.delay_expire_time = otp_data.get("delay_expire")
        if self.delay_expire_time < timezone.now():
            cache.delete(cache_key)
            return True
        return False
