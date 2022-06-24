FROM python:3.10.4

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=/src

WORKDIR /src

RUN apt update \
&& apt install -y --no-install-recommends less

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
