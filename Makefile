up:
	docker compose up --build
alembic-revision:
	docker compose exec api sh -c "python -m alembic revision -m \"$(m)\" --autogenerate --rev-id \"$(rev-id)\""
alembic-upgrade:
	docker compose exec api sh -c "python -m alembic upgrade head"
alembic-downgrade:
	docker compose exec api sh -c "python -m alembic downgrade -1"
adduser:
	docker compose exec api sh -c "python cli.py adduser $(params)"

test-backend:
	cd backend && poetry run pytest -v

test-backend-w-db:
	cd backend && ENGAGE_BACKEND_TESTS__TEST_DATABASE=true poetry run pytest -v

start-test-db:
	docker compose up -d database

migrate:
	cd backend/src && poetry run python -m alembic upgrade head

stop-test-db:
	docker compose down
