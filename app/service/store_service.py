import uuid

from fastapi import Depends, UploadFile
from minio import Minio

from app.config.minio import get_store
from app.config.settings import get_settings, Settings


class StoreService:
    def __init__(self,
                minio: Minio = Depends(get_store),
                settings: Settings = Depends(get_settings)):
        self.minio = minio
        self.settings = settings

    async def save(self, file: UploadFile) -> str:
        if not file:
            return None

        id = str(uuid.uuid4())
        size = len(file.file.read())
        file.file.seek(0)

        self.minio.put_object(self.settings.minio_bucket, id, file.file, size, content_type=file.content_type)
        return id

    def delete(self, url: str) -> bool:
        if not url:
            return False

        id = url.split("/")[-1].split(".")[0]
        self.minio.remove_object(self.settings.minio_bucket, id)
        return True
