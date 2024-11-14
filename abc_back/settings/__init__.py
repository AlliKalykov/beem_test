from .base import Base
from .ci import CI
from .develop import Dev


try:
    from .local import Local
except ImportError:
    LOCAL_CONFIGURATION_EXISTS = False
else:
    LOCAL_CONFIGURATION_EXISTS = True

__all__ = [
    "Base",
    "Dev",
    "CI",
]

if LOCAL_CONFIGURATION_EXISTS:
    __all__ += ["Local"]
