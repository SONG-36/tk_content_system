FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN addgroup --system app && \
    adduser --system --ingroup app --home /home/app app

COPY pyproject.toml ./

RUN python - <<'PY'
import subprocess
import sys
import tomllib
from pathlib import Path

project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
dependencies = project["project"]["dependencies"]
subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "--no-cache-dir", *dependencies]
)
PY

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./
COPY deploy/entrypoint.sh ./deploy/entrypoint.sh

RUN mkdir -p /data/database /data/mock_storage && \
    chown -R app:app /app /data && \
    chmod +x /app/deploy/entrypoint.sh

USER app

EXPOSE 8000

ENTRYPOINT ["/app/deploy/entrypoint.sh"]
