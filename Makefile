# Contrato de comandos do projeto. Rode a partir da raiz, com o venv do backend ativo
# (ou passe PYTHON=backend/.venv/Scripts/python no Windows).
F ?= F00
COMPOSE = docker compose
PYTHON ?= python
PYTEST = $(PYTHON) -m pytest

up:
	$(COMPOSE) up -d --build --wait
down:
	$(COMPOSE) down
migrate:
	$(COMPOSE) exec api alembic upgrade head
migration:
	$(COMPOSE) exec api alembic revision --autogenerate -m "$(MSG)"
seed:
	$(COMPOSE) exec api python -m app.seed
api-client:
	cd frontend && npm run gerar-cliente-api

lint:
	$(PYTHON) -m ruff check --config backend/pyproject.toml backend tests conftest.py
	$(PYTHON) -m ruff format --check --config backend/pyproject.toml backend tests conftest.py
	cd frontend && npm run lint
typecheck:
	cd backend && $(PYTHON) -m mypy app
	cd frontend && npm run typecheck
test:
	$(PYTEST) backend/tests/unit backend/tests/integration -q
test-slice:
	$(PYTEST) tests/acceptance/$(F) -q
test-perms:
	$(PYTEST) tests/permissions -q
test-contract:
	$(PYTEST) tests/contracts -q
e2e:
	cd frontend && npx playwright test
evals:
	$(PYTHON) -m tests.evals.rodar

check: lint typecheck test test-perms test-contract
	$(PYTEST) tests/acceptance -q

.PHONY: up down migrate migration seed api-client lint typecheck test test-slice test-perms test-contract e2e evals check
