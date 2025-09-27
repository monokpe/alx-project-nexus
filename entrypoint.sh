#!/bin/sh

# Wait for the database to be ready
# Use environment variables from docker-compose
until pg_isready -h db -p 5432 -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"; do
  echo "Waiting for database..."
  sleep 2
done

# Run database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run the main command (passed from docker-compose)
exec "$@"