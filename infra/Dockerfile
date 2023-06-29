FROM python:3.10.12-alpine3.17 as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as compile
RUN apk add curl postgresql-dev gcc python3-dev musl-dev
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml poetry.* /app/

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="${PATH}:/root/.local/bin"
RUN cd /app && poetry install

FROM base AS runner

WORKDIR /app

RUN apk add libpq-dev
COPY --from=compile /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ADD ./src  /app/src
ADD ./*.py /app/
ADD ./settings.toml /app/

EXPOSE 8080
CMD ["/bin/sh", "-c", "uvicorn run:app --port 8080 --host 0.0.0.0 --log-level error"]
