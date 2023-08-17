# Project conventions

This file contains some information about the general project conventions aside from the naming conventions.
For naming conventions see [naming_conventions.md](naming_conventions.md).

## Project structure

The project is split into frontend and backend which have their own folders in the root directory.
Additionally there is a `docs` folder which contains documentation and a `scripts` folder which contains scripts to
help with development.

## Frontend

## Backend

- route prefixes for the api should be defined in `backend/src/api/app.py`
- model FastAPI (version >= 0.95) dependency injection should be used. This means
  that dependencies should be injected using the type annotation and the `Annotated` type
  instead of assigning default values to function arguments with `=Depends(...)`.
- Use standard collections for type hinting where possible, i.e. `list[int]` instead of `List[int]`.
- Uses `pydantic>=2` as a major dependency.
- The minimum treatment of enum data should involve the use of `Literal` types. Otherwise its fine to
  use strings as data types until the need for more stability arises.
