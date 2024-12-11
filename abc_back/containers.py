from dependency_injector import containers, providers

from abc_back.cart.containers import CartContainer
from abc_back.pages.containers import PageContainer
from abc_back.products.containers import ProductContainer
from abc_back.users.containers import UserContainer


class Container(containers.DeclarativeContainer):
    """Контейнер с зависимостями проекта."""

    # Domain

    user_package = providers.Container(UserContainer)
    product_package = providers.Container(ProductContainer)
    page_package = providers.Container(PageContainer)
    cart_package = providers.Container(CartContainer)
