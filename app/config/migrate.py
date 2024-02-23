from sqlalchemy.orm import DeclarativeBase

from app.config.database import engine
from app.model.model import Model


def migrate():
    Model.metadata.create_all(engine)
