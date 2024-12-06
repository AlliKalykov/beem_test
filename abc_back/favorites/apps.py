from django.apps import AppConfig


class FavoritesConfig(AppConfig):
    name = "abc_back.favorites"
    verbose_name = "Избранное"
    verbose_name_plural = "Избранное"

    def ready(self):
        from abc_back import container

        container.wire(
            modules=[
                ".admin",
                # "abc_back.api.v1.favorites.views",
            ],
        )
