### Hexlet tests and linter status:
[![Actions Status](https://github.com/tpl-86/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/tpl-86/python-project-52/actions)

Task Manager — учебное веб‑приложение на **Django** для управления задачами.
В проекте реализованы аутентификация пользователей, CRUD для задач/статусов/меток и фильтрация задач. Для продакшена подключён мониторинг ошибок через **Rollbar**.


Демо: https://python-project-52-zs8b.onrender.com

Возможности

- Пользователи: регистрация, вход/выход, список пользователей и управление (CRUD).
- Статусы: CRUD + защита от удаления, если статус используется в задачах.
- Метки (labels): CRUD + защита от удаления, если метка используется в задачах.
- Задачи: CRUD, поля:
  - название, описание
  - статус
  - автор
  - исполнитель
  - метки (many-to-many)
- Фильтрация задач (django-filter): по статусу, исполнителю, метке и «только мои задачи».
- Flash‑сообщения об успехе/ошибках.
- Статика в проде через WhiteNoise.
- Rollbar (трекинг ошибок через переменные окружения).

Технологии:

- Python 3.12+
- Django 5.2.x
- uv (окружение и зависимости)
- dj-database-url (настройка БД через `DATABASE_URL`)
- python-dotenv (`.env`)
- django-filter
- django-bootstrap5
- whitenoise
- rollbar

Установка и запуск (локально):

1) Клонирование

```bash
git clone https://github.com/tpl-86/python-project-52.git
cd python-project-52
```

2) Виртуальное окружение и зависимости (uv)

```bash
uv venv
source .venv/bin/activate
uv sync
```

> Windows (PowerShell):
>
> ```powershell
> .venv\Scripts\activate
> ```

3) Переменные окружения

Создайте файл `.env` в корне проекта.

Минимальный пример для локального запуска:

```env
SECRET_KEY=change-me
DEBUG=True

Можно не задавать — по умолчанию будет SQLite: db.sqlite3
DATABASE_URL=sqlite:///db.sqlite3

ALLOWED_HOSTS=127.0.0.1,localhost

Rollbar (опционально локально)
ROLLBAR_ACCESS_TOKEN=
ROLLBAR_ENVIRONMENT=development
ROLLBAR_BRANCH=main
```

Пояснения:
- `SECRET_KEY` обязателен (в `config/settings.py` читается из окружения).
- `DEBUG` — строка `True/False` (в настройках используется проверка `== 'True'`).
- `DATABASE_URL` — если задан, будет использован; иначе применяется SQLite по умолчанию:
  `sqlite:///.../db.sqlite3`.
- `ALLOWED_HOSTS` — берётся из env и по умолчанию равен `*` (если переменная не задана).
- `RENDER_EXTERNAL_HOSTNAME` — используется на Render (если задан, добавляется в `ALLOWED_HOSTS`).

4) Миграции и суперпользователь

```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

5) (Опционально) Загрузка фикстур

```bash
uv run python manage.py loaddata users/fixtures/users.json
uv run python manage.py loaddata statuses/fixtures/statuses.json
uv run python manage.py loaddata labels/fixtures/labels.json
uv run python manage.py loaddata tasks/fixtures/tasks.json
```

6) Запуск сервера

```bash
uv run python manage.py runserver
```

Откройте:
- Приложение: http://127.0.0.1:8000/
- Админка: http://127.0.0.1:8000/admin/

Тестирование:

```bash
uv run python manage.py test
```

Деплой (Render):

В репозитории есть `render.yaml` и `build.sh`.

На уровне Django уже учтено:
- чтение `DATABASE_URL` через `dj_database_url`
- `ALLOWED_HOSTS` из переменной окружения (по умолчанию `*`)
- поддержка `RENDER_EXTERNAL_HOSTNAME`
- раздача статики через WhiteNoise (`STATIC_ROOT=staticfiles`, `STATIC_URL=/static/`)

Переменные окружения, которые обычно задаются на Render:
- `SECRET_KEY`
- `DEBUG=False`
- `DATABASE_URL` (PostgreSQL)
- `ALLOWED_HOSTS` (если нужно ограничить)
- `ROLLBAR_ACCESS_TOKEN` (опционально)
- `ROLLBAR_ENVIRONMENT=production`
- `ROLLBAR_BRANCH=main`

Примечание по БД:
- В `config/settings.py` при наличии `DATABASE_URL` включается SSL для подключения к БД:
  `OPTIONS = {'sslmode': 'require'}`.

Rollbar (трекинг ошибок):

Rollbar инициализируется из переменных окружения:
- `ROLLBAR_ACCESS_TOKEN`
- `ROLLBAR_ENVIRONMENT` (по умолчанию `development`)
- `ROLLBAR_BRANCH` (по умолчанию `main`)

Для продакшена установите `DEBUG=False` и задайте токен Rollbar.