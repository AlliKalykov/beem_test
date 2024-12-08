from django.apps import AppConfig


class QuestionaryConfig(AppConfig):
    name = "abc_back.questionary"
    verbose_name = "Анкета"
    verbose_name_plural = "Анкеты"

    def ready(self):
        from abc_back import container

        container.wire(
            modules=[
                ".admin",
                "abc_back.api.v1.questionary.views",
            ],
        )
