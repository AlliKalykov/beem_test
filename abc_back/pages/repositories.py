from __future__ import annotations

from abc_back.exceptions import NotFoundError

from .models import AboutUs, Contact, Delivery, GiftCertificate


class PageRepository:
    """Репозиторий для работы с данными пользователей."""

    def get_featured_about_us(self) -> AboutUs:
        try:
            return AboutUs.objects.get(is_featured=True)
        except AboutUs.DoesNotExist:
            raise NotFoundError("Страница не найдена")

    def get_featured_delivery(self) -> Delivery:
        try:
            return Delivery.objects.get(is_featured=True)
        except Delivery.DoesNotExist:
            raise NotFoundError("Страница не найдена")

    def get_featured_gift_certificate(self) -> GiftCertificate:
        try:
            return GiftCertificate.objects.get(is_featured=True)
        except GiftCertificate.DoesNotExist:
            raise NotFoundError("Страница не найдена")

    def get_featured_contact(self) -> Contact:
        try:
            return Contact.objects.get(is_featured=True)
        except Contact.DoesNotExist:
            raise NotFoundError("Страница не найдена")
