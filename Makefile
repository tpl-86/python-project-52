build:
	./build.sh
render-start:
	uv run python -m gunicorn config.wsgi

lint:
	uv run ruff check