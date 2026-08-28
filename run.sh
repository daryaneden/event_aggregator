#!/bin/bash

set -e

uv run celery \
  -A app.infrastructure.celery.app:celery_app \
  worker \
  --loglevel=info &

exec uv run uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000