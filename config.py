"""
Application configuration.

Three environments are supported: development, testing and production.
The active environment is selected through the FLASK_ENV environment
variable so that no secret or machine-specific value is hard-coded.
"""
import os
from pathlib import Path

basedir = Path(__file__).resolve().parent


class BaseConfig:
    """Settings shared by every environment."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-insecure-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INSTANCE_PATH = basedir / "instance"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{basedir / 'instance' / 'bellbird-dev.sqlite3'}",
    )


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(BaseConfig):
    DEBUG = False
    # Production deployments must supply DATABASE_URL (typically a
    # Postgres URL provided by the host). Fail loudly if it is missing.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        # Heroku / Render style DATABASE_URL uses the postgres:// scheme
        # which SQLAlchemy no longer accepts; rewrite it.
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )


CONFIG = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
