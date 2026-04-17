.PHONY: up down logs demo lint migrate

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
	python -m py_compile $$(rg --files -g '*.py')

