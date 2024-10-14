from dependency_injector import containers, providers

from . import repositories, services


class UserContainer(containers.DeclarativeContainer):
    """Контейнер с зависимостями приложения."""

    user_repository = providers.Singleton(
        repositories.UserRepository,
    )
    email_otp_service = providers.Singleton(services.EmailOTPService)
    user_service = providers.Singleton(
        services.UserService,
        user_repository=user_repository,
    )
