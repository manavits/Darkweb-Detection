from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate

from .config import Config, validate_config

# Initialize extensions
db = SQLAlchemy()
mail = Mail()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
migrate = Migrate()

def create_app():
    app = Flask(__name__)  # Fixed: use __name__ (not _name_)
    app.config.from_object(Config)
    validate_config(app)

    # Initialize extensions with app
    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.auth_routes import auth
    from app.routes.admin_routes import admin
    from app.routes.routes import main

    app.register_blueprint(auth)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(main)

    return app
