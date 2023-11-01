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

## Run the backend locally

There are two main ways to run the backend locally. Inside docker and outside of docker.
Running the backend inside of docker is closer to dev and production, but has the disadvantage of
additional build time. This is recommended for situations when one does not directly work
on the backend itself. For instance when one works on the frontend. A local deployment outside
of docker is most helpful when one works on the backend itself and wants hot reloads.

### Run the backend inside docker

In project root run

    make up
    make alembic-upgrade
    make adduser

### Run the backend outside docker

To run the backend you need to have a postgres instance running. The easiest
way to get one is to use out pre-configured docker-compose file in the project root.
This can be used by going to the project root and running.

    make start-test-db

This will start a postgres instance with user `engage` the password `pass` and expose the
default port `5432` on the host.

The default .env file will be sufficient to start a local backend and does not need to be edited.
That being said, the database host will however be dynamically overwritten by make commands
to account for fact that the backend does not run in a docker network.

Before we start the backend we have to deal with the empty database and we'll need to
run the migrations to create the tables. To do this we'll go to the project root folder and run

    make run-local-db-upgrade

Usually we also need a user for API operations. To create a test user we can run

    make create-local-test-user

This creates a user `testuser@example.com` with the password `testpassword123`.

Finally to run the backend use

    make start-local-backend

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
