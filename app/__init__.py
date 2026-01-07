import os
from flask import Flask
from app.database import db

def create_app():
    app = Flask(__name__)

    # ==========================
    # CONFIGURACIÓN BASE DE DATOS
    # ==========================
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        # PRODUCCIÓN (Render / PostgreSQL)
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    else:
        # LOCAL (SQLite)
        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, "..", "instance", "helpdesk.db")
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar DB
    db.init_app(app)

    # Importar modelos ANTES de create_all
    from app.models.ticket import Ticket

    with app.app_context():
        db.create_all()

    # Registrar blueprints
    from app.routes.ticket import ticket_bp
    app.register_blueprint(ticket_bp, url_prefix="/tickets")

    return app
