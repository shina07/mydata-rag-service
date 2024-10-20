FROM python:3.10.14-slim AS builder

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY mrs-core/ /mrs-core
COPY mrs-backend-api/pyproject.toml mrs-backend-api/poetry.lock /app/
WORKDIR /app

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --only main --no-root

FROM python:3.10.14-slim AS runtime

ENV DEBIAN_FRONTEND=noninteractive \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update --fix-missing
RUN apt-get install -y software-properties-common net-tools curl procps supervisor vim

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY mrs-backend-api/deployment/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN mkdir -p /app
COPY mrs-backend-api/deployment/gunicorn /app/gunicorn
COPY mrs-backend-api/README.md mrs-backend-api/pyproject.toml mrs-backend-api/Dockerfile /app/
COPY mrs-backend-api/env /app/env
COPY mrs-backend-api/src /app/src

WORKDIR /app

CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
