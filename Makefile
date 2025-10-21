build:
	./build.sh
render-start:
	uv run python -m gunicorn config.wsgi

lint:
	uv run ruff check

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic

install:
	uv pip install .