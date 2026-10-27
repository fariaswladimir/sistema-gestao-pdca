# Contrato de comandos do projeto. A F00 (tarefa T1) implementa cada alvo.
F ?= F00
COMPOSE = docker compose

up:            ; $(COMPOSE) up -d --build
down:          ; $(COMPOSE) down
migrate:       ; $(COMPOSE) exec api alembic upgrade head
migration:     ; $(COMPOSE) exec api alembic revision --autogenerate -m "$(MSG)"
seed:          ; $(COMPOSE) exec api python -m app.seed
api-client:    ; cd frontend && npm run gerar-cliente-api

lint:          ; cd backend && ruff check . && ruff format --check . ; cd frontend && npm run lint
typecheck:     ; cd backend && mypy app ; cd frontend && npm run typecheck
test:          ; cd backend && pytest tests/unit tests/integration -q
test-slice:    ; cd backend && pytest ../tests/acceptance/$(F) -q
test-perms:    ; cd backend && pytest ../tests/permissions -q
test-contract: ; cd backend && pytest ../tests/contracts -q
e2e:           ; cd frontend && npx playwright test
evals:         ; cd backend && python -m tests.evals.rodar

check: lint typecheck test test-perms test-contract
	cd backend && pytest ../tests/acceptance -q

.PHONY: up down migrate migration seed api-client lint typecheck test test-slice test-perms test-contract e2e evals check
