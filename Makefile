.PHONY: install migrate collectstatic build render-start run dev

install:
	uv sync

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi


dev:
	uv run python manage.py runserver

lint:
	uv run ruff check