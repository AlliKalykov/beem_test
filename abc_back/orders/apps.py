from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = "abc_back.orders"
    verbose_name = "Заказ"
    verbose_name_plural = "Заказы"

    def ready(self):
        from abc_back import container

        container.wire(
            modules=[
                ".admin",
                # "abc_back.api.v1.orders.views",
            ],
        )
