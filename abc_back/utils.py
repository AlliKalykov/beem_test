import os
import pathlib
import uuid
from functools import partial
from random import sample


def generate_filename(__filename: str | os.PathLike | None = None, /) -> str:
    filename = str(uuid.uuid4())
    if __filename and (suffix := pathlib.Path(__filename).suffix):
        filename = f"{filename}{suffix}"
    return filename


def generate_code(length: int = 4) -> str:
    """Возвращает строку из n случайных чисел."""
    return "".join([str(x) for x in sample(range(10), length)])


def set_attrs(obj=None, /, **attrs):
    if obj is None:
        return partial(set_attrs, **attrs)
    for name, value in attrs.items():
        setattr(obj, name, value)
    return obj
