from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject

from abc_back.celery import app
from abc_back.containers import Container


if TYPE_CHECKING:
    from .services import EmailOTPService


@app.task(bind=True, ignore_result=True, time_limit=2 * 60)
@inject
def send_otp_token_email(
    _,
    email: str,
    otp: str,
    email_otp_service: EmailOTPService = Provide[Container.user_package.email_otp_service],
) -> None:
    """Отправка пользователю письма с OTP-токеном."""
    email_otp_service.send_otp_token_email(email=email, otp=otp)
