from __future__ import annotations

import traceback
from typing import TYPE_CHECKING, Callable, ClassVar

from celery import Celery, beat
from celery.app.task import Task as BaseTask
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django.core.cache import cache
from django_celery_beat.schedulers import DatabaseScheduler as _DatabaseScheduler


if TYPE_CHECKING:
    from celery.result import AsyncResult

    from django.core.cache.backends.base import BaseCache

from configurations.importer import installed


if not installed:
    import configurations
    configurations.setup()


from django.conf import settings  # noqa: E402


class Task(BaseTask):
    # True, если одномоментно может существовать только одна такая задача (запущенная или в ожидании, не важно).
    lock: ClassVar[bool] = False

    # Уникальная часть ключа лока: None, кортеж или callable, возвращающее кортеж.
    lock_suffix: ClassVar[tuple | Callable[..., tuple] | None] = None

    # Максимальное время жизни лока на повторный запуск задачи, секунды.
    lock_ttl: ClassVar[int | None] = None

    log = get_task_logger(__name__)

    _cache: BaseCache | None = None

    __original_run: ClassVar[Callable]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if cls.lock_suffix or cls.lock_ttl:
            cls.lock = True
        if cls.lock:
            if not cls.lock_ttl:
                cls.lock_ttl = settings.CELERY_DEFAULT_TASK_LOCK_TTL
            cls.__original_run = cls.run
            cls.run = cls.__wrapped_run

    def __wrapped_run(self, *args, **kwargs):
        # Хук on_failure не подходит для освобождения лока, потому что при autoretry вызывается не после каждого
        # падения таска, а только после последнего рейтрая.
        # Хук on_retry не подходит для освождения лока, потому что вызывается *после* повторного планирования
        # таска (apply_async), когда уже поздно.
        # Кастомный __call__ тоже не подходит, потому что при autoretry механизм авторетрая реализован оборачиванием
        # оригинального run в ретраящий враппер (соответственно, в __call__ в finally уже поздно релизить лок).
        # Единственная (?) оставшаяся возможность вмещаться в механизм авторетраев — обернуть враппер во враппер,
        # что мы собственно и делаем тут.
        try:
            return self.__original_run(*args, **kwargs)
        finally:
            self._maybe_unset_lock(task_id=self.request.id, args=args, kwargs=kwargs)

    @property
    def cache(self) -> BaseCache:
        if self._cache is None:
            self._cache = self.get_cache()
        return self._cache

    def get_cache(self) -> BaseCache:
        return cache

    def apply_async(self, args=None, kwargs=None, *, force: bool = False, **options) -> AsyncResult:
        if not self.lock:
            return super().apply_async(args=args, kwargs=kwargs, **options)
        lock_key = self._format_lock_key(args, kwargs)
        if not force:
            task_id = self._read_lock(lock_key)
            if task_id:
                self.log.debug("[%s] is already set", lock_key)
                return self.AsyncResult(task_id)
        else:
            self.log.debug("force=True, ignoring [%s]", lock_key)
        result = super().apply_async(args=args, kwargs=kwargs, **options)
        self._set_lock(lock_key, result.id)
        self.log.debug("[%s] has been set for task instance [%s]", lock_key, result.id)
        return result

    def delay(self, *args, force: bool = False, **kwargs) -> AsyncResult:
        return self.apply_async(args, kwargs, force=force)

    def _maybe_unset_lock(self, task_id: str, args: tuple, kwargs: dict) -> None:
        if not self.lock:
            return
        lock_key = self._format_lock_key(args, kwargs)
        stored_task_id = self._read_lock(lock_key)
        if not stored_task_id:
            return
        if stored_task_id == task_id:
            pass
            # Временно отключено. Затирает
            # self._unset_lock(lock_key)
            # self.log.debug("[%s] has been unset", lock_key)
        else:
            self.log.debug("[%s] is set for another task instance [%s], ignoring", lock_key, stored_task_id)

    @classmethod
    def _format_lock_key(cls, args: tuple | None = None, kwargs: dict | None = None) -> str:
        if lock_suffix := cls.lock_suffix:
            if callable(lock_suffix):
                if args is None:
                    args = ()
                if kwargs is None:
                    kwargs = {}
                lock_suffix = lock_suffix(*args, **kwargs)
                assert isinstance(lock_suffix, (tuple, list))
        else:
            lock_suffix = ()
        assert cls.name
        return ":".join(("task", cls.name, *map(str, lock_suffix), "lock"))

    def _set_lock(self, lock_key: str, task_id: str) -> None:
        self.cache.set(lock_key, task_id, timeout=self.lock_ttl)

    def _unset_lock(self, lock_key: str) -> None:
        self.cache.delete(lock_key)

    def _read_lock(self, lock_key: str) -> str | None:
        return self.cache.get(lock_key)


class DatabaseScheduler(_DatabaseScheduler):
    """Переопределенный Beat Scheduler для корректной обработки задач с локом."""

    def apply_entry(self, entry, producer=None) -> None:
        beat.info("Scheduler: Sending due task %s (%s)", entry.name, entry.task)
        try:
            result = self.apply_async(entry, producer=producer, advance=False)
        except Exception as exc:  # pylint: disable=broad-except
            beat.error("Message Error: %s\n%s", exc, traceback.format_stack(), exc_info=True)
        else:
            if result is not None:
                beat.debug("%s sent. id->%s", entry.task, result.id)
            else:
                beat.debug("Task %s is locked", entry.task)


app = Celery(__package__, task_cls=Task)
app.config_from_object(settings.CELERY)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
}
