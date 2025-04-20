#!/usr/bin/env bash

set -e

echo '[alembic] Updating to a latest version...'

yes y | poetry run litestar --app main:app database upgrade

echo
echo '[alembic] Done!'

# Execute command
$@