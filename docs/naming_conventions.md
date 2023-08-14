# Naming conventions

This file contains the naming conventions used in the project.
We try to stick to the conventions and new pull requests should follow them.
That being said, there might be some exceptions to naming conventions, especially in older code.
Naming conventions might have changed/ were established only after some code has been written.
We should try to update the code to follow the conventions, where simple renaming can be done
along with other changes, but complicated renaming should be done in dedicated pull requests.

## Singular vs plural

- table names: plural
- endpoint names: plural
- model names: singular
- schema names: singular

## Environment names

We distinguish between the following environments:

- production: the production environment running on a vps
- development: the development environment running on a vps
- local: the local development environment running on a local machine
