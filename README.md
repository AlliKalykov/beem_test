# ABC Concierge

## Настройка и запуск

Docker конфигурации содержат контейнеры:
  1. nginx
  2. postgres
  3. gunicorn
  4. celery
  5. celery-beat
  6. redis

Для успешного запуска необходимо указать переменные окружения в файле `.env` в корне проекта.

**Формат `.env` файла:**

```dotenv
ENV=.env

DJANGO_SETTINGS_MODULE=abc_back.settings
DJANGO_CONFIGURATION=Local (Возможные: Local, Test, Stage)
SECRET_KEY=

PROJECT_BASE_URL=http://localhost:8080
PROJECT_ENVIRONMENT=local (Возможные: local, test, stage)

ALLOWED_HOSTS=localhost
CSRF_TRUSTED_ORIGINS=http://localhost:8080,https://localhost:8080

MEDIA_URL=media/
STATIC_URL=/staticfiles/

POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

REDIS_CACHE_URL=redis://redis:6379/1
REDIS_BROKER_URL=redis://redis:6379/2

NGINX_DOMAIN=localhost
NGINX_PROJECT_NAME=abc_back

# SMTP
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_SSL=True (default)
EMAIL_USE_TLS =False (default)

# Celery
FLOWER_PORT=8888
CELERY_FLOWER_HOST_PORT=8888
FLOWER_URL_PREFIX=flower

# Admin
SUPERUSER_LOGIN=admin@mail.ru
SUPERUSER_PASSWORD=yuek)rfrfqk

# S3 Storage (при подключении django-storages)
STATIC_S3_LOCATION=static
MEDIA_S3_LOCATION=media

# AWS settings
AWS_PRIVATE_STORAGE_BUCKET_NAME=xxx
AWS_STORAGE_BUCKET_NAME=xxx
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_S3_ENDPOINT_URL=https://storage.yandexcloud.net
AWS_S3_REGION_NAME=ru-central1
AWS_S3_SIGNATURE_VERSION=s3v4
AWS_S3_FILE_OVERWRITE=False
AWS_S3_VERIFY=True
AWS_QUERYSTRING_AUTH=True

# Синхронизация (optional, можно не указывать, ниже отражены дефолтные значения)
SYNC_USER_STATS_LOCK_TTL=300
SYNC_COURSES_AND_PROGRAMS_LOCK_TTL=300
SYNC_EVENTS_AND_WEBINAR_TTL=300
```

**Формат `.env` файла продакшн:**

```dotenv
ENV=.env

DJANGO_SETTINGS_MODULE=apsb.settings
DJANGO_CONFIGURATION=Production
DJANGO_ADMIN=django-cadmin
SECRET_KEY=
PIP_EXTRA_INDEX_URL=https://pypi-user:Ohkie9Xa@pypi.teachbasetest.ru/

PROJECT_BASE_URL=http://localhost:8080
PROJECT_ENVIRONMENT=production

ALLOWED_HOSTS=localhost
CSRF_TRUSTED_ORIGINS=http://localhost:8080,https://localhost:8080

MEDIA_URL=media/
STATIC_URL=/staticfiles/

POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

REDIS_CACHE_URL=redis://redis:6379/1
REDIS_BROKER_URL=redis://redis:6379/2

TEACHBASE_CLIENT_ID=
TEACHBASE_CLIENT_SECRET=
TEACHBASE_USER_AUTH_URL=https://apsb-test.teachbase.ru/accounts/52255/user_auth

# SMTP
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_SSL=True (default)
EMAIL_USE_TLS =False (default)

# Celery
FLOWER_PORT=8888
CELERY_FLOWER_HOST_PORT=8888
FLOWER_URL_PREFIX=flower

# Admin
SUPERUSER_LOGIN=admin@teachbase.ru
SUPERUSER_PASSWORD=yuek)rfrfqk

# S3 Storage (при подключении django-storages)
STATIC_S3_LOCATION=static
MEDIA_S3_LOCATION=media

# AWS settings
AWS_PRIVATE_STORAGE_BUCKET_NAME=xxx
AWS_STORAGE_BUCKET_NAME=xxx
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_S3_ENDPOINT_URL=https://storage.yandexcloud.net
AWS_S3_REGION_NAME=ru-central1
AWS_S3_SIGNATURE_VERSION=s3v4
AWS_S3_FILE_OVERWRITE=False
AWS_S3_VERIFY=True
AWS_QUERYSTRING_AUTH=True

# Sentry
SENTRY_DNS=
```

Доступы от администратора в админ. панель по дефолту (можно изменить добавив соответствующие переменные окружения):
```dotenv
SUPERUSER_LOGIN=admin@teachbase.ru
SUPERUSER_PASSWORD=yuek)rfrfqk
```

При использовании flower сервиса - добавить:
```dotenv
# Celery | Flower
FLOWER_PORT=8888
FLOWER_HOST_PORT=8888
FLOWER_URL_PREFIX=flower
```
**Запуск производится в два этапа:**

```
docker-compose -f docker-compose-local.yml build
docker-compose -f docker-compose-local.yml up
```

*При первом запуске могут быть проблемы с миграциями. Это лечится запуском миграций в отдельных приложениях:

```
docker-compose -f docker-compose-local.yml run --rm server bash
django-cadmin migrate users
django-cadmin migrate django_celery_beat
django-cadmin migrate
```

При старте gunicorn контейнера выполняется применение миграций и сбор статики.

Перезапуск контейнеров вручную происходит в один этап:

```
docker-compose -f docker-compose-local.yml restart
```

В проекте используется [`django-configurations`](https://django-configurations.readthedocs.io/en/latest/), поэтому для выполнения management команд Django вместо `./manage.py` / `python -m django` / `django-admin` следует использовать `django-cadmin`.

## Разработка

Синхронизировать окружение с `requirements.txt` / `requirements.dev.txt` (установит отсутствующие пакеты, удалит лишние, обновит несоответствующие версии):

```shell
make sync-requirements
```

Перегенерировать `requirements.txt` / `requirements.dev.txt` (требуется после изменений в `requirements.in` / `requirements.dev.in`):

```shell
make compile-requirements
```

Если в окружении требуется установить какие-либо пакеты, которые нужно только локально разработчику, то следует создать файл `requirements.local.in` и указывать зависимости в нём. Обязательно следует указывать constraints files (`-c ...`). Например, чтобы запускать `shell_plus` c `ptipython` (`django-cadmin shell_plus --ptipython`), нужно поставить пакеты `ipython` и `ptpython`, в таком случае файл `requirements.local.in` будет выглядеть примерно так (первые строки одинаковы для всех, остальное — зависимости для примера):

```
-c requirements.txt
-c requirements.dev.txt

ipython >=7, <8
ptpython >=3, <4
```

Перед пушем коммита следует убедиться, что код соответствует принятым стандартам и соглашениям:

```shell
make lint
```

Перед пушем коммита следует включить автоправку:

```shell
make fix
```

## Документация API

Документация в формате OpenAPI 3 доступна по адресу:

* `${PROJECT_BASE_URL}/api/v1/schema` (YAML или JSON, выбор через content negotiation заголовком `Accept`)
* `${PROJECT_BASE_URL}/api/v1/schema/redoc` (ReDoc)
* `${PROJECT_BASE_URL}/api/v1/schema/swagger-ui` (Swagger UI)
