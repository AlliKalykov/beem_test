from dependency_injector import containers, providers

from . import repositories


class PageContainer(containers.DeclarativeContainer):
    """Контейнер с зависимостями приложения."""

    page_repository = providers.Singleton(
        repositories.PageRepository,
    )
