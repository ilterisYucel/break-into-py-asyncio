FROM python:3.11-alpine AS base

ENV VIRTUAL_ENV=/inovat-device/.venv \
    PATH="/inovat-device/.venv/bin:$PATH"

RUN apk update && apk add libpq

FROM base AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apk update && apk add musl-dev build-base gcc gfortran openblas-dev

WORKDIR /inovat-device

# Install Poetry
RUN pip install poetry==1.8.3

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry install && rm -rf "$POETRY_CACHE_DIR"

# The runtime image, used to just run the code provided its virtual environment
FROM base AS runtime

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY device ./device
COPY tests ./tests
COPY configuration.yaml ./configuration.yaml


CMD ["python", "-m", "device"]
