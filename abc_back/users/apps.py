from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "abc_back.users"
    verbose_name = "Пользователи"

    def ready(self):
        from abc_back import container

        container.wire(
            modules=[
                ".tasks",
                ".managers",
                ".admin",
                "abc_back.api.v1.users.views",
                # "abc_back.mails.tasks",
            ],
        )
