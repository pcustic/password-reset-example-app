from __future__ import annotations

from flask_login import UserMixin
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from werkzeug.security import generate_password_hash, check_password_hash

from flask import current_app


from app import db, login


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"

    def generate_reset_password_token(self) -> str:
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

        return serializer.dumps(self.email, salt=self.password_hash)

    @staticmethod
    def validate_reset_password_token(token: str, user_id: int):
        # Check if there exists a user with this id.
        user = db.session.get(User, user_id)

        if user is None:
            return None

        # Now that we now the user exists we can check the validity of the token.
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            token_user_email = serializer.loads(
                token,
                max_age=current_app.config["RESET_PASS_TOKEN_MAX_AGE"],
                salt=user.password_hash,
            )
        except (BadSignature, SignatureExpired):
            return None

        # As an addition we check that deserialized email from the token matches the email from the database.
        if token_user_email != user.email:
            return None

        return user


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
