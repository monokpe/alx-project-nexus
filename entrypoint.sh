#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to parse DATABASE_URL and export PG* variables
parse_database_url() {
  if [ -n "$DATABASE_URL" ]; then
    eval $(python -c "
import os
from urllib.parse import urlparse

result = urlparse(os.environ['DATABASE_URL'])
print(f'export PGHOST={result.hostname}')
print(f'export PGPORT={result.port}')
print(f'export PGUSER={result.username}')
print(f'export PGPASSWORD={result.password}')
print(f'export PGDATABASE={result.path[1:]}')
")
  fi
}

# Parse DATABASE_URL to set PG* environment variables
parse_database_url

# Wait for the database to be ready
until pg_isready; do
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