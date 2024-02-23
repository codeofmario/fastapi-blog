from typing import List
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.model.model import Model
from app.model.user_role import user_role_table


class Role(Model):
    __tablename__ = 'roles'
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)

    users: Mapped[List["User"]] = relationship("User", secondary=user_role_table, back_populates='roles')
