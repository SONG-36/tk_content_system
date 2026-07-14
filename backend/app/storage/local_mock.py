"""Local filesystem storage for Phase 2A mock uploads."""

from __future__ import annotations

import os
from pathlib import Path


class LocalMockStorage:
    """Writes assets atomically under a controlled local directory."""

    EXTENSIONS = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "video/mp4": ".mp4",
    }

    def __init__(self, base_directory: str) -> None:
        self.base_directory = Path(base_directory).expanduser().resolve()

    def path_for(self, *, asset_id: str, content_type: str) -> Path:
        extension = self.EXTENSIONS[content_type]
        filename = f"{asset_id}{extension}"
        path = (self.base_directory / filename).resolve()
        if path.parent != self.base_directory:
            raise ValueError("Resolved path escaped storage directory.")
        return path

    def write_atomic(self, *, asset_id: str, content_type: str, data: bytes) -> str:
        self.base_directory.mkdir(parents=True, exist_ok=True)
        final_path = self.path_for(asset_id=asset_id, content_type=content_type)
        temp_path = final_path.with_name(f".{final_path.name}.tmp")
        try:
            with open(temp_path, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, final_path)
        except Exception:
            temp_path.unlink(missing_ok=True)
            raise
        return str(final_path)

    def write_result_atomic(
        self, *, asset_id: str, content_type: str, data: bytes
    ) -> str:
        result_storage = LocalMockStorage(str(self.base_directory / "results"))
        return result_storage.write_atomic(
            asset_id=asset_id,
            content_type=content_type,
            data=data,
        )

    @property
    def result_base_directory(self) -> Path:
        return (self.base_directory / "results").resolve()

    def resolve_result_path(self, storage_path: str) -> Path:
        path = Path(storage_path).expanduser().resolve()
        try:
            path.relative_to(self.result_base_directory)
        except ValueError as exc:
            raise ValueError("Resolved result path escaped results directory.") from exc
        return path

    def delete(self, storage_path: str) -> None:
        path = Path(storage_path).expanduser().resolve()
        try:
            path.relative_to(self.base_directory)
        except ValueError:
            return
        path.unlink(missing_ok=True)

    def cleanup_temp_files(self) -> None:
        if not self.base_directory.exists():
            return
        for path in self.base_directory.glob(".*.tmp"):
            path.unlink(missing_ok=True)
