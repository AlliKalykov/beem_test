from dependency_injector import containers, providers


from abc_back.users.containers import UserContainer


class Container(containers.DeclarativeContainer):
    """Контейнер с зависимостями проекта."""

    # Domain

    user_package = providers.Container(UserContainer)

