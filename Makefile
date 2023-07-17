up:
	docker compose up --build
alembic-revision:
	docker compose exec api sh -c "python -m alembic revision -m \"$(m)\" --autogenerate --rev-id \"$(rev-id)\""
alembic-upgrade:
	docker compose exec api sh -c "python -m alembic upgrade head"
alembic-downgrade:
	docker compose exec api sh -c "python -m alembic downgrade -1"
