FROM python:3.10-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update \
        && apt-get install -y --no-install-recommends build-essential default-libmysqlclient-dev libmariadb-dev


# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime
COPY wait-for-it.sh /
# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
RUN apt-get update \
        && apt-get install -y --no-install-recommends default-libmysqlclient-dev \
        unzip curl procps  \
        && apt-get clean \
        && apt-get autoremove -y \
        && chmod +x /wait-for-it.sh

ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home fastapi
WORKDIR /home/fastapi
USER fastapi

# Install application into container
COPY . .
USER root
RUN chown fastapi:fastapi stemmi campioncini backup tmp

# Run the application
USER fastapi

ENTRYPOINT ["python"]
CMD [ "cli.py","run"]
