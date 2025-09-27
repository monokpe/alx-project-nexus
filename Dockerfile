# --- Builder Stage ---
# This stage installs dependencies
FROM python:3.11-slim-bookworm AS builder
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- NEW: Install system dependencies required for building Python packages ---
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    pkg-config \
    && apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Final Stage ---
# This stage builds the final, smaller production image
FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Create a non-root user for security
RUN adduser --system --group appuser

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application code
COPY . .

# Run collectstatic to gather all static files
# The --noinput flag is important for non-interactive builds
RUN python manage.py collectstatic --noinput

# Change ownership of files to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# The command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "nexus.wsgi:application"]
