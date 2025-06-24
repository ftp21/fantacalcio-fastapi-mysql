FROM python:3.10-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential default-libmysqlclient-dev libmariadb-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade "pipenv<2023.10.0"

COPY Pipfile Pipfile.lock ./
ENV PIPENV_VENV_IN_PROJECT=1
RUN pipenv install --deploy || true \
 && $(pipenv --venv)/bin/pip install "pip<24.1" \
 && pipenv install --deploy

FROM base AS runtime

COPY wait-for-it.sh /
COPY --from=python-deps /.venv /.venv

RUN apt-get update \
    && apt-get install -y --no-install-recommends default-libmysqlclient-dev unzip curl procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && chmod +x /wait-for-it.sh

ENV PATH="/.venv/bin:$PATH"

RUN useradd --create-home fastapi
WORKDIR /home/fastapi
USER fastapi

COPY . .

USER root
RUN mkdir -p stemmi

ENTRYPOINT ["python"]
CMD [ "cli.py","run"]
