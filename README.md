# CorrelAid Engage

CorrelAid engage is a tool intended to help with the management of projects that
are often done with partner organizations. The tools aims to help with the
organization of the whole project life cycle. It is currently
in development and not yet ready for production use.

The main entities in the system tracks are:

- Projects
- Partner organizations
- Project members

In addition the tool aims to offer two different levels of access:

- Admins: Can create and edit all entities
- Team Admins: Can create and edit all entities for their team

## Project structure

The project is split into a frontend and a backend. The frontend is a Vue.js app and the backend is a python app using FastAPI. Storage is done in a Postgres database.

To see how to setup the development environment for the frontend and backend see the respective READMEs in the `frontend` and `backend` folders.

## Selected Makefile commands

In this section we only aim to provide a short overview of the most important commands. For a full list of commands see the `Makefile`.

- `make up`: Starts the backend development environment in docker

## Dev Deployment

To make a dev deployment of the backend you need to

1.  Log into the dev server instance

1.  Clone the repository

1.  Go to the project folder and checkout the branch you want to deploy

1.  Make a copy of the `.env` file

        cp .env .env.dev

1.  Update the `.env` file with the desired values. Additionally the following
    variables for the database need need to be set:

        POSTGRES_USER=
        POSTGRES_DB=
        POSTGRES_PASSWORD=

    Their values have to be the same as the ones set for the `ENAGE_BACKEND_DATABASE`
    environment variables in the same file.

1.  Set up caddy

        TBD

1.  Run the following make command.

        make build-and-start-dev-frontend-backend
        make start-dev-database

    This will build and start the frontend and backend containers. The backend will run on port `8000` and the frontend on port `8080`.

1.  To apply migrations and create database users execute the following commands inside he backend container.

        python -m alembic upgrade head
        python cli.py adduser

    Or equivalently outside of a container

        docker exec engage-api python -m alembic upgrade head
        docker exec engage-api run python cli.py adduser
