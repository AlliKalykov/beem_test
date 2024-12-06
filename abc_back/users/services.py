import logging
import uuid
from datetime import timedelta
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.template.loader import render_to_string
from django.utils import timezone

from abc_back.infrastructure.mail.messages import EmailMessage
from abc_back.types import Id
from abc_back.utils import generate_code

from .constants import (
    BAD_ATTEMPTS_COUNT, BAN_TIME_MINUTES, OTP_TOKEN_EXPIRED, OTP_TOKEN_INVALID, OTP_TOKEN_SEND_DELAY_TIME_MINUTES,
    OTP_TOKEN_VALID, OTP_TOKEN_VALIDATION_TIME_MINUTES,
)
from .repositories import UserRepository


logger = logging.getLogger(__name__)

UserModel = get_user_model()


class EmailOTPService:
    """Сервис для работы с email-токенами."""

    def create_token(self, data: dict) -> dict[str, str | Any]:
        """Создание OTP-токена."""
        from .tasks import send_otp_token_email

        email = data["email"]
        otp = generate_code(length=6)
        uid = str(uuid.uuid4())
        used = False
        created_at = timezone.now()
        delay_expire = timezone.now() + timedelta(minutes=OTP_TOKEN_SEND_DELAY_TIME_MINUTES)
        cache.set(
            f"otpcode:{email}",
            {"otp": otp, "uid": uid, "used": used, "created_at": created_at, "delay_expire": delay_expire},
            OTP_TOKEN_VALIDATION_TIME_MINUTES * 60,
        )
        send_otp_token_email.delay(email, otp)
        if settings.DEBUG:
            # для тестового окружения отдавать код подтверждения в респонсе
            return {"email": email, "uid": uid, "otp": otp}
        return {"email": email, "uid": uid}

    def validate_token(self, data: dict) -> tuple[bool, str | None]:
        """Валидация email-токена."""
        email = data.get("email")
        otp = data.get("otp")
        uid = data.get("uid")
        created_diff = timezone.now() - timedelta(minutes=OTP_TOKEN_VALIDATION_TIME_MINUTES)
        token = cache.get(f"otpcode:{email}")
        if not token:
            return False, OTP_TOKEN_INVALID
        if (token["otp"] == otp) and (token["uid"] == uid) and (token["used"] is False):
            if token["created_at"] >= created_diff:
                return True, OTP_TOKEN_VALID
            return False, OTP_TOKEN_EXPIRED
        self.set_otp_prove_data(email)
        return False, OTP_TOKEN_INVALID

    def get_or_create_user(self, data: dict) -> tuple[UserModel | None, bool]:
        """Создание/получение пользователя по otp-токену и email."""
        email = data.get("email", False)
        if not email:
            return None, False
        uid = data.get("uid")
        otp = data.get("otp")
        token = cache.get(f"otpcode:{email}")
        if not token or (token["otp"] != otp) or (token["uid"] != uid):
            return None, False
        cache.delete(f"otpcode:{email}")
        user: UserModel = UserModel.objects.filter(email=email).first()
        if not user:
            user: UserModel = UserModel.objects.create_user(email=email)
        if user.first_name == "" and user.last_name == "":
            return user, False
        return user, True

    @staticmethod
    def set_otp_prove_data(email: str) -> None:
        """Создание/обновление данных об ip."""
        cache_key = f"otpprove:{email}"
        cache_data = cache.get(cache_key)
        if cache_data is None:
            cache_data = {"unblock_time": None, "count": 1}
            cache.set(cache_key, cache_data)
            return
        cache_data["count"] += 1
        if cache_data["count"] >= BAD_ATTEMPTS_COUNT:
            cache_data["unblock_time"] = timezone.now() + timedelta(minutes=BAN_TIME_MINUTES)
        cache.set(cache_key, cache_data, BAN_TIME_MINUTES * 60)

    def send_otp_token_email(self, email: str, otp: str) -> None:
        """Отправка письма с OTP-токеном пользователю на почту."""
        context = {"otp": otp}
        html_content = render_to_string("users/email_otp/email_confirm.html", context)
        email_message = EmailMessage(
            subject="Авторизация на платформе",
            body=html_content,
            to=[email],
            from_email=f"ABC Concierge <{settings.DEFAULT_FROM_EMAIL}>",
        )
        email_message.send()


class UserService:
    """Сервис для работы с пользователями."""

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self._user_repository = user_repository

    def change_user_email_by_id(self, user_id: Id, new_email: str) -> None:
        """Смена почты пользователя по его ID."""
        user = self._user_repository.get_by_pk(user_id)
        user.email = new_email
        user.save(update_fields=["email"])

    def activate_by_id(self, user_id: Id) -> None:
        user = self._user_repository.get_by_pk(user_id)
        user.is_active = True
        user.save(update_fields=["is_active"])

    def delete_by_id(self, user_id: Id) -> None:
        user = self._user_repository.get_by_pk(user_id)
        user.delete()

    def update_user_by_id(self, user_id: Id, **kwargs) -> None:
        user = self._user_repository.get_by_pk(user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save(update_fields=kwargs.keys())

    def update_last_login(self, user_id: Id) -> None:
        user = self._user_repository.get_by_pk(user_id)
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

    def create_user(self, email: str, password: str, **kwargs) -> UserModel:
        """Создание пользователя."""
        return self._user_repository.create_user(email=email, password=password, **kwargs)
