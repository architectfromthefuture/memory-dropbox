.PHONY: up down logs demo lint migrate test compose-config

up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

migrate:
	alembic upgrade head

demo:
	python scripts/demo.py

lint:
	python -m ruff check packages apps
	python -m compileall -q packages apps

test:
	pytest

compose-config:
	docker compose config --quiet
