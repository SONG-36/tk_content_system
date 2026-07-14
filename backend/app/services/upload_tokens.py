"""Upload token generation and hashing."""

from __future__ import annotations

import hashlib
import secrets


def generate_upload_token(token_bytes: int) -> str:
    """Generate a URL-safe upload capability token."""

    if token_bytes < 32:
        raise ValueError("upload_token_bytes must be at least 32.")
    return secrets.token_urlsafe(token_bytes)


def hash_upload_token(token: str) -> str:
    """Hash an upload token before lookup or persistence."""

    return hashlib.sha256(token.encode("utf-8")).hexdigest()
