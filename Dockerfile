FROM python:3.9-slim-buster

RUN mkdir /app
WORKDIR /app

RUN pip install pipenv && pipenv install

CMD ['uvicorn', 'app:app --reload --port 5555']
