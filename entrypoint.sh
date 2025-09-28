#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e
set -x

echo "--- Starting entrypoint.sh ---"

# Function to parse DATABASE_URL and export PG* variables
parse_database_url() {
  echo "--- Parsing DATABASE_URL ---"
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
  echo "--- Finished parsing DATABASE_URL ---"
}

# Parse DATABASE_URL to set PG* environment variables
parse_database_url

# Wait for the database to be ready
echo "--- Waiting for database ---"
until pg_isready; do
  echo "Waiting for database..."
  sleep 2
done
echo "--- Database is ready ---"

# Run database migrations
echo "--- Applying database migrations ---"
python manage.py migrate
echo "--- Finished applying database migrations ---"

# Collect static files
echo "--- Collecting static files ---"
python manage.py collectstatic --no-input
echo "--- Finished collecting static files ---"

# Run the main command (passed from docker-compose)
echo "--- Starting application ---"
exec "$@"