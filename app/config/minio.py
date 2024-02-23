from typing import Generator

from minio import Minio

from app.config.settings import get_settings

# Get settings
settings = get_settings()


def get_store() -> Generator:
    client = Minio(
        f"{settings.minio_endpoint}:{settings.minio_port}",
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=False
    )
    yield client
