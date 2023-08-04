# Engange Backend

The goal of the engage backend is to provide a REST Api that can be sued by the
engage frontend. The backend is written in python and uses FastAPI as the main
library to build the REST Api.

For storage the backend assumes a connection to a Postgres instance.

## Dev env setup

1. Go to the backend folder

1. Install with poetry

        poetry install

1. Install pre-commit hooks

        poetry run pre-commit install -c ../.pre-commit-config.yaml

1. To run all pre-commit hooks for all files use

        poetry run pre-commit run -c ../.pre-commit-config.yaml --all-files

    When run for the first time this should configure and run all hooks. The
    checks from the hooks should pass for a freshly cloned repository.

## Run the backend

To run the backend you need to have a postgres instance running. The easiest
way to get one is to use docker.

    docker run --name engage-postgres -e POSTGRES_PASSWORD=engage -p 5432:5432 -d postgres

This will start a postgres instance with the password `engage` and expose the
default port `5432` on the host. The database will be empty and we'll need to run the migrations to create the tables.

    TBD

Before running the backend you need to set the environment variables. The following variables are required:

    CSRF_SECRET=...
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=engage
    POSTGRES_DB=postgres

The `CSRF_SECRET` is used to sign the CSRF token. It can be any string. The
`POSTGRES_USER` and `POSTGRES_PASSWORD` are the credentials for the postgres
instance. The `POSTGRES_DB` is the name of the database to use.

To run the backend use

    poetry run python src/main.py

## Testing

Currently there are two modes for testing set up.
1. Testing without a database
2. Testing with a test database

To test without a database the user can run

    poetry run pytest

or equivalently in the project root

    make test-backend

This will run all the tests that are not related to the database
and skip the rest.

To test with a testing database a testing database
a local database instance has to be started and the latest
migrations have to be applied. Otherwise the database can still be
empty and the tests will populate it with data as needed.
One straight forward way to start a database is
1. Go to project root and start the backend

        make start-test-db

2. In a separate terminal apply the migrations

        make migrate

To run the database tests, the environment variable `ENGAGE_BACKEND_TESTS__TEST_DATABASE`
must be set to true. Pytest can then either be run directly

    poetry run pytest

or the make command that also sets the mentioned env variable can be used

    make backend-test-w-db

Once the testing is done the database can be stopped with

    docker compose down

or equivalently

    make stop-test-db
