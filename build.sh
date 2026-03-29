#!/usr/bin/env bash
# Render / production build: collect static assets for WhiteNoise (admin, Jazzmin, site CSS/JS).
set -euo pipefail
python manage.py collectstatic --noinput
