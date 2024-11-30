from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = "abc_back.pages"
    verbose_name = "Страница"
    verbose_name_plural = "Страницы"

    def ready(self):
        from abc_back import container

        container.wire(
            modules=[
                ".admin",
                # "abc_back.api.v1.users.views",
            ],
        )
