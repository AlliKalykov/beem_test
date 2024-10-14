from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from celery import Celery

    from abc_back.containers import Container


container: Container
app: Celery


def __getattr__(name):
    from configurations.importer import installed
    if not installed:
        import configurations
        configurations.setup()

    if name in ["celery_app", "app"]:
        from .celery import app
        return app

    if name != "container":
        raise AttributeError(name)

    from abc_back.containers import Container

    global container
    container = Container()
    return container
