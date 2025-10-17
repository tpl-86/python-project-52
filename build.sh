#!/usr/bin/env bash
# скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

echo "--> Installing dependencies with uv..."
uv pip sync --no-cache

echo "--> Collecting static files..."
poetry run python manage.py collectstatic --no-input --clear

echo "--> Applying database migrations..."
poetry run python manage.py migrate