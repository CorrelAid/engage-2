FROM python:3.11 AS builder

ENV POETRY_VERSION=1.3.2
ARG ENVIRONMENT=DEVELOPMENT

RUN pip install poetry==$POETRY_VERSION
RUN poetry config virtualenvs.create false
RUN if [ "$ENVIRONMENT" = "DEVELOPMENT" ]; then pip install debugpy; else echo "Debugging will not be available." ; fi

COPY poetry.lock pyproject.toml ./
RUN if [ "$ENVIRONMENT" = "DEVELOPMENT" ]; then poetry install; else poetry install --no-dev; fi

COPY ./src /app
COPY  ./pyproject.toml /app


FROM python:3.11-slim as api

COPY --from=builder /app /app
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
WORKDIR /app
