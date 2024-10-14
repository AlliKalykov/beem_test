from typing import Final, List

from django.db import models
from django.db.models import TextChoices

BAN_TIME_MINUTES: Final[int] = 15
BAD_ATTEMPTS_COUNT: Final[int] = 5
OTP_TOKEN_EXPIRED: Final[str] = "expired"
OTP_TOKEN_INVALID: Final[str] = "invalid"
OTP_TOKEN_VALID: Final[str] = "valid"
OTP_TOKEN_VALIDATION_TIME_MINUTES: Final[int] = 15
OTP_TOKEN_SEND_DELAY_TIME_MINUTES: Final[int] = 1


USER_AVATAR_ALLOWED_EXTENSIONS = ["jpeg", "jpg", "png"]
USER_AVATAR_MAX_UPLOAD_SIZE = 5 * 1024 * 1024


class UserGenderChoices(TextChoices):
    MALE = "M", "Мужской"
    FEMALE = "F", "Женский"
