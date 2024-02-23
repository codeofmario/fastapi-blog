from typing import Optional, List
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.model.comment import Comment
from app.model.model import Model
from app.model.post import Post
from app.model.role import Role
from app.model.user_role import user_role_table


class User(Model):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    avatar_id: Mapped[Optional[str]] = mapped_column(unique=True, index=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=False, nullable=False)

    roles: Mapped[List["Role"]] = relationship("Role", secondary=user_role_table, back_populates='users')
    posts: Mapped[List["Post"]] = relationship()
    comments: Mapped[List["Comment"]] = relationship()
