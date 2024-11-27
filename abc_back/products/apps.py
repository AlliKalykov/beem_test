from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = "abc_back.products"
    verbose_name = "Товар"
    verbose_name_plural = "Товары"

    def ready(self):
        from abc_back import container

        container.wire(
            modules=[
                ".managers",
                ".admin",
                "abc_back.api.v1.products.views",
                # "abc_back.mails.tasks",
            ],
        )
