#!/bin/bash

alembic upgrade head

echo "Start backend process"

python3 -m uvicorn backend.presentation.web.main:app --host 0.0.0.0 --reload
