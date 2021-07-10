
FROM python:3.9-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update \
        && apt-get install -y --no-install-recommends build-essential default-libmysqlclient-dev libmariadbclient-dev


# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
COPY --from=python-deps /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home fastapi
WORKDIR /home/fastapi
USER fastapi

# Install application into container
COPY . .

# Run the application

ENTRYPOINT ["python"]
CMD [ "run.py"]
