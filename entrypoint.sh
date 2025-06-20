#!/bin/sh

set -e

alembic upgrade head

python src/main.py

