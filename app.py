"""Application entry point.

Run locally with:
    flask --app app run
"""
import os
from flask import Flask, render_template

from config import CONFIG
from extensions import db, migrate


def create_app(config_name: str | None = None) -> Flask:
    """Application-factory pattern so we can spin up isolated instances
    for tests and for production deployments without importing globals."""
    app = Flask(__name__, instance_relative_config=True)

    config_name = config_name or os.environ.get("FLASK_ENV", "default")
    app.config.from_object(CONFIG[config_name])

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (imported here to avoid circular imports).
    from blueprints.inventory import bp as inventory_bp
    from blueprints.orders import bp as orders_bp
    from blueprints.customers import bp as customers_bp
    from blueprints.reports import bp as reports_bp

    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(reports_bp, url_prefix="/reports")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


app = create_app()

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
