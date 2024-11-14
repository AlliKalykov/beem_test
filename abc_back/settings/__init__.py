from .base import Base
from .develop import Dev
from .ci import CI


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
