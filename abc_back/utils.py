from __future__ import annotations

import os
import pathlib
import uuid
from functools import partial
from random import sample
from typing import TYPE_CHECKING

from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.safestring import mark_safe


if TYPE_CHECKING:
    from django.db import models
    from django.utils.safestring import SafeString


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


def join_url(url: str, query: str | dict) -> str:
    if isinstance(query, dict):
        query = urlencode(query)
    return f"{url}?{query}"


def render_html_link(url: str, content: str | None = None, *, new_tab: bool = False) -> SafeString:
    return format_html(
        "<a href='{url}'{target}>{content}</a>",
        url=url,
        target=mark_safe(" target='_blank'" if new_tab else ""),
        content=content or url,
    )


def get_object_changelist_url(obj: models.Model, query: str | dict | None = None) -> str:
    model_label = obj._meta.label_lower.replace(".", "_")
    url = reverse(f"admin:{model_label}_changelist")
    if query:
        return join_url(url, query)
    return url


def render_object_changelist_link(
    obj: models.Model, content: str | None = None, *, query: str | dict | None = None, new_tab: bool = False,
) -> SafeString:
    return render_html_link(url=get_object_changelist_url(obj, query), content=content or str(obj), new_tab=new_tab)
