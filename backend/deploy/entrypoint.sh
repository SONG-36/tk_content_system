#!/usr/bin/env sh
set -eu

require_env() {
  name="$1"
  value="$(eval "printf '%s' \"\${$name:-}\"")"
  if [ -z "$value" ]; then
    echo "Missing required environment variable: $name" >&2
    exit 1
  fi
}

require_env BACKEND_API_KEY
require_env BACKEND_OWNER_ID
require_env BACKEND_DATABASE_URL
require_env BACKEND_PUBLIC_BASE_URL
require_env BACKEND_MOCK_STORAGE_DIRECTORY
require_env BACKEND_RESULT_TOKEN_SECRET

if [ "$BACKEND_API_KEY" = "$BACKEND_RESULT_TOKEN_SECRET" ]; then
  echo "BACKEND_API_KEY and BACKEND_RESULT_TOKEN_SECRET must differ." >&2
  exit 1
fi

mkdir -p /data/database /data/mock_storage

python - <<'PY'
import os

from alembic import command
from alembic.config import Config

config = Config("/app/alembic.ini")
config.set_main_option("script_location", "/app/alembic")
config.set_main_option("sqlalchemy.url", os.environ["BACKEND_DATABASE_URL"])
command.upgrade(config, "head")
PY

exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
