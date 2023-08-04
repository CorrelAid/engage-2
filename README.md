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
