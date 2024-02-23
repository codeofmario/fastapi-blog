from typing import List

from sqlalchemy import ForeignKey, types
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.model.comment import Comment
from app.model.model import Model


class Post(Model):
    __tablename__ = 'posts'

    title: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(types.Text, nullable=False)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship()
