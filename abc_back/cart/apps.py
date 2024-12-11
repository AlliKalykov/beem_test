from django.apps import AppConfig


class CartConfig(AppConfig):
    name = "abc_back.cart"
    verbose_name = "Корзина"
    verbose_name_plural = "Корзины"

    def ready(self):
        from abc_back import container

        container.wire(
            modules=[
                ".admin",
                "abc_back.api.v1.cart.views",
            ],
        )
