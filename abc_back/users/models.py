from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from abc_back.utils import generate_filename
from abc_back.validators import MaxFileSizeValidator, NameValidator, validate_date_of_birth, validate_email

from .constants import USER_AVATAR_ALLOWED_EXTENSIONS, USER_AVATAR_MAX_UPLOAD_SIZE, UserGenderChoices
from .managers import ActiveUserManager, UserManager


BASE_USERS_MEDIA_FOLDER = "users"


def user_avatar_upload_to(instance, filename) -> str:
    new_filename = generate_filename(filename)
    return f"{BASE_USERS_MEDIA_FOLDER}/avatar/{new_filename}"


class User(AbstractUser):
    """Пользователь на проекте."""

    username = None
    USERNAME_FIELD = EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": "Пользователь с таким email адресом уже зарегистрирован.",
            "invalid": "Пожалуйста, введите корректный email.",
        },
        validators=[validate_email],
    )
    first_name = models.CharField(_("first name"), max_length=36, blank=True, validators=[NameValidator()])
    last_name = models.CharField(_("last name"), max_length=36, blank=True, validators=[NameValidator()])
    middle_name = models.CharField(
        "Отчество",
        max_length=36,
        blank=True,
        null=True,
        validators=[NameValidator()],
    )

    date_of_birth = models.DateField(
        verbose_name="Дата рождения",
        blank=True,
        null=True,
        validators=[validate_date_of_birth],
    )

    gender = models.CharField(verbose_name="Пол", choices=UserGenderChoices.choices, max_length=1, blank=True)

    phone = PhoneNumberField(verbose_name="Телефон", unique=True, blank=True, null=True)

    profile_image = models.ImageField(
        verbose_name="Изображение профиля", upload_to=user_avatar_upload_to, null=True, blank=True, max_length=512,
        validators=[
            MaxFileSizeValidator(USER_AVATAR_MAX_UPLOAD_SIZE),
            FileExtensionValidator(allowed_extensions=USER_AVATAR_ALLOWED_EXTENSIONS),
        ],
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()
    active = ActiveUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def is_administrator(self):
        return self.is_superuser

    def has_flower_permission(self) -> bool:
        return self.is_administrator

    def get_full_name(self) -> str:
        return " ".join(filter(None, [self.last_name, self.first_name]))
