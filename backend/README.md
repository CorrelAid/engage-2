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
