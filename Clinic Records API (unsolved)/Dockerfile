FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY src/ .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run application
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]