from sqlalchemy import ForeignKey, Table, Column

from app.model.model import Model

user_role_table = Table(
    "user_role",
    Model.metadata,
    Column("user_id", ForeignKey("users.id", ondelete='CASCADE'), index=True),
    Column("role_id", ForeignKey("roles.id", ondelete='CASCADE'), index=True),
)
