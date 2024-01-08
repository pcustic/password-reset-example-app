import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "really-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", ""
    ) or "sqlite:///" + os.path.join(basedir, "app.db")

    RESET_PASS_TOKEN_MAX_AGE = int(
        os.environ.get("RESET_PASS_TOKEN_MAX_AGE") or (15 * 60)
    )

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)

    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = (
        os.environ.get("MAIL_DEFAULT_SENDER") or "do-not-reply@pass-reset-example.com"
    )
