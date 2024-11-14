from typing import NamedTuple, TypeVar

from django.db.models import Model


Id = int

_Model = TypeVar("_Model", bound=Model)


class ModelInfo(NamedTuple):
    """Информация о модели в проекте."""

    app_name: str
    model_name: str
