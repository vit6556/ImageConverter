#!/bin/sh

echo "Waiting for postgres connection"
while ! nc -z image_converter_postgres 5432; do
    sleep 0.1
done
echo "PostgreSQL started"

exec "$@"