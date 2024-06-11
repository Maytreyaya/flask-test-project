FROM python:3.9-slim as base

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists

WORKDIR /app
#
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN #pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0"]