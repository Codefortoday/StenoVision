import hashlib
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

from app.core.config import settings

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".dcm", ".nii", ".nii.gz"}
CHUNK_SIZE = 1024 * 1024  # read uploads 1 MB at a time


class UnsupportedFileTypeError(Exception):
    """The file extension is not on the allow-list."""


class FileTooLargeError(Exception):
    """The upload is bigger than MAX_UPLOAD_MB."""


@dataclass
class StoredFile:
    key: str
    size_bytes: int
    sha256: str


def get_extension(filename: str) -> str:
    name = filename.lower()
    if name.endswith(".nii.gz"):  # Path.suffix would only return ".gz"
        return ".nii.gz"
    return Path(name).suffix


class LocalStorage:
    def __init__(self, root: str) -> None:
        self.root = Path(root).resolve()

    def save(self, fileobj: BinaryIO, filename: str, case_id: int) -> StoredFile:
        extension = get_extension(filename)
        if extension not in ALLOWED_EXTENSIONS:
            raise UnsupportedFileTypeError(extension)

        # The stored name is random: the user's filename never touches the disk path.
        key = f"cases/{case_id}/{uuid.uuid4().hex}{extension}"
        path = self.root / key
        path.parent.mkdir(parents=True, exist_ok=True)

        max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
        hasher = hashlib.sha256()
        size = 0
        try:
            with path.open("wb") as out:
                while chunk := fileobj.read(CHUNK_SIZE):
                    size += len(chunk)
                    if size > max_bytes:
                        raise FileTooLargeError(settings.MAX_UPLOAD_MB)
                    hasher.update(chunk)
                    out.write(chunk)
        except Exception:
            path.unlink(missing_ok=True)  # never keep a half-written file
            raise

        return StoredFile(key=key, size_bytes=size, sha256=hasher.hexdigest())

    def resolve(self, key: str) -> Path:
        path = (self.root / key).resolve()
        if not path.is_relative_to(self.root) or not path.is_file():
            raise FileNotFoundError(key)
        return path

    def delete(self, key: str) -> None:
        try:
            self.resolve(key).unlink()
        except FileNotFoundError:
            pass


storage = LocalStorage(settings.STORAGE_ROOT)