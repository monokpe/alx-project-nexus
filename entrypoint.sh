#!/bin/sh

# Wait for the database to be ready
until pg_isready -h db -p 5432 -U admin -d nexus_db; do
  echo "Waiting for database..."
  sleep 2
done

# Run the main command
exec "$@"
