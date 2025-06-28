# main.py
from flask import Flask
from flasgger import Swagger
from core.config import Config
from core.extensions import db, ma
from app.routes.user_routes import user_bp
from core.error_handlers import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apidocs/apispec_1.json',
                "rule_filter": lambda rule: True,  # Documentar todas las rutas
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    Swagger(app, config=swagger_config)

    app.register_blueprint(user_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    register_error_handlers(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
