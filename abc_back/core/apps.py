from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "abc_back.core"
    verbose_name = "Основные"
    verbose_name_plural = "Основные"

    def ready(self):
        from abc_back import container

        container.wire(
            modules=[
                ".admin",
                # "abc_back.api.v1.orders.views",
            ],
        )
