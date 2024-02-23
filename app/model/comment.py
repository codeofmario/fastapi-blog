from sqlalchemy import ForeignKey, types
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.model.model import Model


class Comment(Model):
    __tablename__ = 'comments'

    body: Mapped[str] = mapped_column(types.Text, nullable=False)

    # Relationships
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="comments")

    post_id: Mapped[str] = mapped_column(ForeignKey("posts.id"))
    post = relationship("Post", back_populates="comments")
