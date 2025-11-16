FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc curl git && \
    rm -rf /var/lib/apt/lists/*

# Install pip and dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy app
COPY . /app

# Create a non-root user
RUN useradd --create-home appuser
USER appuser
WORKDIR /home/appuser

# Copy app to non-root user home
RUN mkdir -p /home/appuser/app
COPY --chown=appuser:appuser . /home/appuser/app
WORKDIR /home/appuser/app

ENV PATH="/home/appuser/.local/bin:${PATH}"

# Collect static (will succeed later in k8s if missing)
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# Note: replace YOUR_DJANGO_PROJECT with the folder that contains wsgi.py
CMD ["gunicorn", "leature3.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-"]
