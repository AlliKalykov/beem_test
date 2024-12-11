from dependency_injector import containers, providers

from . import repositories


class ProductContainer(containers.DeclarativeContainer):
    """Контейнер с зависимостями приложения."""

    product_repository = providers.Singleton(
        repositories.ProductRepository,
    )
    sub_product_repository = providers.Singleton(
        repositories.SubProductRepository,
    )
    category_repository = providers.Singleton(
        repositories.CategoryRepository,
    )
