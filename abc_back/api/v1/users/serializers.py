from rest_framework import serializers

from abc_back.users.models import User


class ProfileShortSerializer(serializers.ModelSerializer):
    """Сериаллайзер для получения данных профиля пользователя."""

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "profile_image",
        ]


class ProfileInfoSerializer(serializers.ModelSerializer):
    """Сериаллайзер для получения данных профиля пользователя."""

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "middle_name", "email", "date_of_birth", "gender", "profile_image",
        ]


class ProfileEditSerializer(serializers.ModelSerializer):
    """Сериаллайзер для изменения простых данных профиля пользователя."""

    class Meta:
        model = User
        fields = [
            "profile_image", "first_name", "last_name", "middle_name", "date_of_birth", "gender",
        ]


class ValidateEmailOTPTokenSerializer(serializers.Serializer):
    """Сериализатор для валидации токена для email."""

    email = serializers.EmailField(label="Почта", required=True)
    otp = serializers.CharField(label="Временный пароль", required=True)
    uid = serializers.UUIDField(label="UUID", required=True)


class LoginSerializer(serializers.Serializer):
    """Сериалайзер для регистрации или входа пользователя."""

    email = serializers.EmailField(label="Почта", required=True)
    password = serializers.CharField(label="Пароль", required=True)


class RegisterSerializer(serializers.Serializer):
    """Сериалайзер для регистрации или входа пользователя."""

    first_name = serializers.CharField(label="Имя", required=True)
    last_name = serializers.CharField(label="Фамилия", required=True)
    middle_name = serializers.CharField(label="Отчество", required=False)
    email = serializers.EmailField(label="Почта", required=True)
    password = serializers.CharField(label="Пароль", required=True)


class LoginResponseSerializer(serializers.Serializer):
    """Сериалайзер для ответа при регистрации или входа пользователя."""

    refresh_token = serializers.CharField(help_text="Токен для обновления токена доступа")
    access_token = serializers.CharField(help_text="Токен доступа")


class EmailSerializer(serializers.Serializer):
    """Сериализатор для создания токена для email."""

    email = serializers.EmailField(label="Почта", required=True)
