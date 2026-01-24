.PHONY: install migrate collectstatic build render-start dev lint test test-coverage check

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
	uv run ruff check .

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=gendiff --cov-report=xml:coverage.xml


check: lint test
