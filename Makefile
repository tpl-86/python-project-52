build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi