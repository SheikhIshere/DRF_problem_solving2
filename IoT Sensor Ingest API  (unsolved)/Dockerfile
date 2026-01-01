# root/App/Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# copy and install requirements
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY ./App /app

# create media dir
RUN mkdir -p /vol/web/media

# ENV DJANGO_SETTINGS_MODULE=App.settings
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
