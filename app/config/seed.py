import bcrypt
from sqlalchemy.orm import Session

from app.config.database import engine
from app.model.role import Role
from app.model.user import User


def seed():
    with Session(bind=engine) as session:
        if not session.query(User).filter_by(username="john").first():
            # create users
            encoded_password = b"password"
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(encoded_password, salt)
            john = User(username="john", email="john@example.com", password=password.decode("utf-8"), is_active=True)
            session.add(john)

            jane = User(username="jane", email="jane@example.com", password=password.decode("utf-8"), is_active=True)
            session.add(jane)

            session.commit()

            # create roles
            role_user = Role(name="ROLE_USER")
            session.add(role_user)

            role_admin = Role(name="ROLE_ADMIN")
            session.add(role_admin)

            session.commit()

            # map users to roles
            john.roles = [role_admin, role_user]
            jane.roles = [role_user]

            session.commit()
