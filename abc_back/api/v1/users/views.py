from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from django.contrib.auth import authenticate, login
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from abc_back.api.constants import ErrorCode
from abc_back.api.serializers import EmptySerializer
from abc_back.api.v1.users.serializers import ProfileEditSerializer, ProfileInfoSerializer
from abc_back.api.views import MultiSerializerViewSetMixin, MultiThrottllesViewSetMixin
from abc_back.containers import Container
from abc_back.users.models import User


if TYPE_CHECKING:
    from abc_back.users.services import EmailOTPService, UserService

from . import openapi
from .serializers import EmailSerializer, LoginSerializer, RegisterSerializer, ValidateEmailOTPTokenSerializer
from .throttles import EmailOTPCreateThrottle, EmailOTPValidationThrottle


class ProfileViewSet(
    MultiSerializerViewSetMixin,
    MultiThrottllesViewSetMixin,
    viewsets.GenericViewSet,
):
    """Viewset для работы с профилем пользователя."""

    queryset = User.objects.none()
    serializer_classes = {
        "profile_info": ProfileInfoSerializer,
        "edit_profile": ProfileEditSerializer,
        "update_email_request": EmailSerializer,
        "update_email_confirm": ValidateEmailOTPTokenSerializer,
        "delete_profile": EmptySerializer,
    }
    throttle_classes = {
        "update_email_request": [EmailOTPCreateThrottle],
        "update_email_confirm": [EmailOTPValidationThrottle],
    }

    @openapi.profile_info
    @action(detail=False, methods=["GET"], url_path="info")
    def profile_info(
        self, request: Request,
    ) -> Response:
        """Данные текущего авторизованного пользователя."""
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data)

    @openapi.edit_profile
    @action(detail=False, methods=["PATCH"], url_path="edit")
    def edit_profile(
        self,
        request: Request,
        user_service: UserService = Provide[Container.user_package.user_service],
    ) -> Response:
        """Изменение данных профиля."""
        serializer = self.get_serializer(self.request.user, data=self.request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
        user_service.update_user_by_id(request.user.pk, **serializer.validated_data)
        return Response(serializer.data)

    @openapi.delete_profile
    @action(detail=False, methods=["DELETE"], url_path="delete")
    def delete_profile(
        self,
        request: Request,
        user_service: UserService = Provide[Container.user_package.user_service],
    ) -> Response:
        """Деактивация пользователя."""
        user_service.delete_by_id(request.user.pk)
        return Response(status=status.HTTP_200_OK)

    @openapi.update_email_request
    @action(detail=False, methods=["PATCH"], url_path="email/change")
    def update_email_request(
        self,
        request: Request,
        email_otp_service: EmailOTPService = Provide[Container.user_package.email_otp_service],
    ) -> Response:
        """Запрос на обновление email."""
        serializer: EmailSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_to_response = email_otp_service.create_token(serializer.data)
        return Response(data=data_to_response, status=status.HTTP_201_CREATED)

    @openapi.update_email_confirm
    @action(methods=["POST"], detail=False, url_path="email/confirm")
    def email_confirm(
        self,
        request: Request,
        email_otp_service: EmailOTPService = Provide[Container.user_package.email_otp_service],
        user_service: UserService = Provide[Container.user_package.user_service],
    ) -> Response:
        """Подтверждение новой почты."""
        serializer: ValidateEmailOTPTokenSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated, message = email_otp_service.validate_token(serializer.data)
        if not validated:
            return Response(data={"otp": [message]}, status=status.HTTP_400_BAD_REQUEST)
        user_service.change_user_email_by_id(request.user.pk, serializer.data.get("email"))
        return Response(status=status.HTTP_200_OK)


class EmailOTPTokenViewSet(
    MultiSerializerViewSetMixin,
    MultiThrottllesViewSetMixin,
    GenericViewSet,
):
    """API для подтверждения email."""

    permission_classes = []

    queryset = None
    serializer_classes = {
        "validate": ValidateEmailOTPTokenSerializer,
    }
    throttle_classes = {
        "create": [EmailOTPCreateThrottle],
        "validate": [EmailOTPValidationThrottle],
    }

    @inject
    def create(
        self,
        request: Request,
        email_otp_service: EmailOTPService = Provide[Container.user_package.email_otp_service],
    ) -> Response:
        """Создание email-токена."""
        serializer: EmailSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_to_response = email_otp_service.create_token(serializer.data)
        return Response(data=data_to_response, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=False)
    def validate(
        self,
        request: Request,
        email_otp_service: EmailOTPService = Provide[Container.user_package.email_otp_service],
    ) -> Response:
        """Валидация email-токена."""
        serializer: ValidateEmailOTPTokenSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated, otp_status = email_otp_service.validate_token(serializer.data)
        message = {"token": otp_status}
        if not validated:
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=message, status=status.HTTP_200_OK)


class UserViewSet(MultiSerializerViewSetMixin, GenericViewSet):
    """Пользователь."""

    serializer_classes = {
        "login": LoginSerializer,
        "register": RegisterSerializer,
    }

    @openapi.login
    @action(methods=["POST"], detail=False, permission_classes=[])
    def login(
        self,
        request: Request,
        user_service: UserService = Provide[Container.user_package.user_service],
    ) -> Response:
        """Регистрация или авторизация пользователя после валидации OTP-кода."""
        serializer: LoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            login(request, user)
            user_service.update_last_login(user.id)
            refresh = RefreshToken.for_user(user)
            return Response(
                data={
                    "refresh_token": str(refresh),
                    "access_token": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        raise exceptions.AuthenticationFailed()

    @openapi.register
    @action(methods=["POST"], detail=False, permission_classes=[])
    def register(
        self, request: Request,
        user_service: UserService = Provide[Container.user_package.user_service],
        email_otp_service: EmailOTPService = Provide[Container.user_package.email_otp_service],
    ) -> Response:
        """Регистрация пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        email_otp_service.create_token(email)
        user = user_service.create_user(email=email, password=password)
        if not user:
            raise ErrorCode.EMAIL_ALREADY_TAKEN.as_exception()
        refresh = RefreshToken.for_user(user)
        return Response(
            data={
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
