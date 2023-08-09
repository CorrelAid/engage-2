BACKEND_START_CMD=gunicorn api.app:app --workers=2 --worker-class=uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --access-logfile -
DOCKER_START_CMD_BASE=docker run -d --rm --network engage-network

.PHONY: up
up:
	docker compose up --build

.PHONY: alembic-revision
alembic-revision:
	docker compose exec api sh -c "python -m alembic revision -m \"$(m)\" --autogenerate --rev-id \"$(rev-id)\""

.PHONY: alembic-upgrade
alembic-upgrade:
	docker compose exec api sh -c "python -m alembic upgrade head"

.PHONY: alembic-downgrade
alembic-downgrade:
	docker compose exec api sh -c "python -m alembic downgrade -1"

.PHONY: adduser
adduser:
	docker compose exec api sh -c "python cli.py adduser $(params)"

.PHONY: test-backend
test-backend:
	cd backend && poetry run pytest -v

.PHONY: test-backend-w-db
test-backend-w-db:
	cd backend && ENGAGE_BACKEND_TESTS__TEST_DATABASE=true poetry run pytest -v

.PHONY: start-test-db
start-test-db:
	docker compose up -d database

.PHONY: stop-test-db
stop-test-db:
	docker compose down

.PHONY: lint
lint:
	cd backend && poetry run pre-commit run -c ../.pre-commit-config.yaml

.PHONY: lint-all
lint-all:
	cd backend && poetry run pre-commit run -c ../.pre-commit-config.yaml --all-files

.PHONY: build-dev-frontend-backend
build-dev-frontend-backend:
	docker build --build-arg ENVIRONMENT=PRODUCTION -t engage-api ./backend
	docker build -t engage-client ./frontend

.PHONY: create-engage-network
create-engage-network:
	(test -z $$(docker network ls --filter name=engage-network -q) \
		&& (docker network create engage-network \
			|| echo "Creating engage-network docker network failed.")) \
	|| echo "engage-network already exists"

.PHONY: start-dev-frontend-backend
start-dev-frontend-backend: create-engage-network
	${DOCKER_START_CMD_BASE} \
		--network-alias api \
		--name engage-api \
		--env-file .env.dev \
		--publish 8000:8000 \
		engage-api:latest sh -c '${BACKEND_START_CMD}' \
		|| echo "Starting engange-api failed."
	${DOCKER_START_CMD_BASE} \
		--network-alias client \
		--name engage-client \
		--publish 8080:80 \
		engage-client:latest \
		|| echo "Starting engange-client failed."

.PHONY: build-and-start-dev-frontend-backend
build-and-start-dev-frontend-backend:
	make build-dev-frontend-backend
	make start-dev-frontend-backend

.PHONY: start-dev-database
start-dev-database: create-engage-network
	${DOCKER_START_CMD_BASE} \
		--network-alias database \
		--name engage-database \
		--env-file .env.dev \
		postgres:13.2 \
		|| echo "Starting engange-database failed."

.PHONY: stop-engage-dev-frontend-backend
stop-engage-dev-frontend-backend:
	docker stop engage-api || echo "Stopping engage-api failed."
	docker stop engage-client || echo "Stopping engage-client failed."
	docker network rm engage-network || echo "Removing engage-network docker network failed."
