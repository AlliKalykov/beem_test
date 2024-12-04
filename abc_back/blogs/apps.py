from django.apps import AppConfig


class BlogsConfig(AppConfig):
    name = "abc_back.blogs"
    verbose_name = "Блог"
    verbose_name_plural = "Блог"

    def ready(self):
        from abc_back import container

        container.wire(
            modules=[
                ".admin",
                # "abc_back.api.v1.users.views",
            ],
        )
