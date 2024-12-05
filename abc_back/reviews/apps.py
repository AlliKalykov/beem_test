from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    name = "abc_back.reviews"
    verbose_name = "Отзыв"
    verbose_name_plural = "Отзывы"

    def ready(self):
        from abc_back import container

        container.wire(
            modules=[
                ".admin",
                # "abc_back.api.v1.reviews.views",
            ],
        )
