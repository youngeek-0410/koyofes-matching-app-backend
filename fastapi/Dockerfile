FROM python:3.10.4

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=/src

WORKDIR /src

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
