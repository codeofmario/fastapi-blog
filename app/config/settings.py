from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    at_secret: str
    rt_secret: str

    redis_host: str
    redis_port: int
    redis_password: str

    minio_endpoint: str
    minio_port: int
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str

    db_url: str
    db_host: str
    db_port: int
    db_name: str
    db_username: str
    db_password: str

    username: str
    password: str
    email: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
