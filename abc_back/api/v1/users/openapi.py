from abc_back.api.openapi import extend_schema

from .serializers import (
    LoginResponseSerializer, LoginSerializer, ProfileEditSerializer, ProfileInfoSerializer, RegisterSerializer,
)


delete_profile = extend_schema(
    summary="Удаление аккаунта.",
    description="Удаление всех персональных данных",
    responses={
        200: None,
    },
)

profile_info = extend_schema(
    summary="Пользовательские данные.",
    description="Получение данных профиля авторизованного пользователя.",
    responses={
        200: ProfileInfoSerializer,
        400: None,
        401: None,
    },
)

edit_profile = extend_schema(
    summary="Изменение пользовательских данных.",
    description="Изменение данных профиля авторизованного пользователя.",
    responses={
        200: ProfileEditSerializer,
        400: None,
        401: None,
    },
)

update_email_request = extend_schema(
    summary="Запрос на смену почты пользователя.",
    description=(
        "Отправляется токен на новую почту, потом ее следует подтвердить.\n"
        "Также присутствует ограничение на отправку запроса - 1 сообщение в 60 секунд"
    ),
    responses={
        201: None,
        400: None,
        429: None,
    },
)

update_email_confirm = extend_schema(
    summary="Подтверждение смены почты пользователя.",
    description=(
        "Подтверждение смены почты после запроса на изменение.\n"
        "После 5 попыток, подтверждения - бан по ip на 15 минут"
    ),
    responses={
        200: None,
        400: None,
        429: None,
    },
)

login = extend_schema(
    summary="Вход пользователя.",
    description="Вход я пользователя.",
    responses={
        200: LoginResponseSerializer,
        400: None,
    },
)

register = extend_schema(
    summary="Регистрация пользователя.",
    description="Регистрация нового пользователя.",
    responses={
        201: LoginResponseSerializer,
        400: None,
    },
)
